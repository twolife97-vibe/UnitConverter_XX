"""변환 CLI 출력 줄 검증 — PRD §1.4 KPI-4·5·6.

| KPI | 본 모듈 | 비고 |
|-----|---------|------|
| KPI-4 | validate_session | 연속 2+ 출력 묶음 |
| KPI-5 | validate_lines(profile=…) | default 4자리 / business m·mm |
| KPI-6 | validate_lines(default) | meter/feet/yard 동시 출력·비율 |

KPI-1·2·3은 범위 밖 — session/continuous, input/entity 각각.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import TypedDict

from src.conversion.meter import format_converted, from_meters, to_meters
from src.registry.profiles import DEFAULT_TARGETS, DISPLAY_DECIMALS, Profile
from src.registry.units import SUPPORTED_UNITS

LINE_RE = re.compile(
    r"^(?P<src_val>\S+)\s+(?P<src_unit>\S+)\s+=\s+(?P<dst_val>\S+)\s+(?P<dst_unit>\S+)$"
)

_INCOMPLETE_MARKERS = (
    "missing target",
    "no output",
    "expected at least",
)


class ValidationResult(TypedDict):
    status: str
    failed_lines: list[str]


@dataclass(frozen=True)
class ParsedLine:
    src_val: float
    src_unit: str
    dst_val: float
    dst_unit: str
    raw_dst_val: str


def _tolerance_for(unit: str, profile: Profile) -> float:
    decimals = DISPLAY_DECIMALS[profile][unit]
    if decimals == 0:
        return 0.5
    return 0.5 * 10 ** (-decimals)


def expected_targets_for(source_unit: str, profile: Profile = "default") -> frozenset[str]:
    return DEFAULT_TARGETS[profile] - {source_unit}


def parse_line(line: str) -> ParsedLine | str:
    line = line.strip()
    if not line:
        return "empty line"
    match = LINE_RE.match(line)
    if not match:
        return f"invalid format: {line!r}"
    try:
        src_val = float(match.group("src_val"))
        dst_val = float(match.group("dst_val"))
    except ValueError:
        return f"invalid number: {line!r}"
    return ParsedLine(
        src_val=src_val,
        src_unit=match.group("src_unit"),
        dst_val=dst_val,
        dst_unit=match.group("dst_unit"),
        raw_dst_val=match.group("dst_val"),
    )


def _collect_errors(
    lines: list[str],
    *,
    source_value: float | None = None,
    source_unit: str | None = None,
    profile: Profile = "default",
    expected_targets: frozenset[str] | set[str] | None = None,
) -> list[str]:
    errors: list[str] = []
    parsed: list[ParsedLine] = []

    for i, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        result = parse_line(line)
        if isinstance(result, str):
            errors.append(f"line {i}: {result}")
            continue
        parsed.append(result)

    if not parsed:
        return errors or ["no output lines"]

    ref = parsed[0]
    if source_value is not None and ref.src_val != source_value:
        errors.append(f"source value mismatch: expected {source_value}, got {ref.src_val}")
    if source_unit is not None and ref.src_unit != source_unit:
        errors.append(f"source unit mismatch: expected {source_unit!r}, got {ref.src_unit!r}")

    targets = (
        frozenset(expected_targets)
        if expected_targets is not None
        else expected_targets_for(ref.src_unit, profile)
    )

    for i, p in enumerate(parsed, start=1):
        if p.src_val != ref.src_val or p.src_unit != ref.src_unit:
            errors.append(
                f"line {i}: left side must echo input ({ref.src_val} {ref.src_unit})"
            )

        if p.src_unit not in SUPPORTED_UNITS:
            errors.append(f"line {i}: unsupported source unit {p.src_unit!r}")
        if p.dst_unit not in SUPPORTED_UNITS:
            errors.append(f"line {i}: unsupported target unit {p.dst_unit!r}")
        if p.dst_unit == p.src_unit:
            errors.append(f"line {i}: target unit must differ from source ({p.dst_unit})")

        expected = format_converted(
            from_meters(to_meters(p.src_val, p.src_unit), p.dst_unit),
            p.dst_unit,
            profile,
        )
        if p.raw_dst_val != expected:
            errors.append(
                f"line {i}: expected {expected} {p.dst_unit}, got {p.raw_dst_val} {p.dst_unit}"
            )
        else:
            tolerance = _tolerance_for(p.dst_unit, profile)
            if abs(p.dst_val - float(expected)) > tolerance:
                errors.append(f"line {i}: conversion out of tolerance for {p.dst_unit}")

    seen_targets = [p.dst_unit for p in parsed]
    if len(seen_targets) != len(set(seen_targets)):
        errors.append("duplicate target units in output")

    actual_targets = frozenset(seen_targets)
    missing = targets - actual_targets
    extra = actual_targets - targets
    if missing:
        errors.append(f"missing target units: {', '.join(sorted(missing))}")
    if extra:
        errors.append(f"unexpected target units: {', '.join(sorted(extra))}")

    return errors


def _to_result(errors: list[str]) -> ValidationResult:
    if not errors:
        return {"status": "pass", "failed_lines": []}
    if any(marker in error.lower() for error in errors for marker in _INCOMPLETE_MARKERS):
        return {"status": "incomplete", "failed_lines": errors}
    return {"status": "fail", "failed_lines": errors}


def validate_lines(
    lines: list[str],
    *,
    source_value: float | None = None,
    source_unit: str | None = None,
    profile: Profile = "default",
    expected_targets: frozenset[str] | set[str] | None = None,
) -> ValidationResult:
    """변환 출력 줄 목록을 검증한다."""
    errors = _collect_errors(
        lines,
        source_value=source_value,
        source_unit=source_unit,
        profile=profile,
        expected_targets=expected_targets,
    )
    return _to_result(errors)


def validate_session(
    output_groups: list[list[str]],
    *,
    min_groups: int = 2,
    profile: Profile = "business",
    source_value: float | None = None,
    source_unit: str | None = None,
    expected_targets: frozenset[str] | set[str] | None = None,
) -> ValidationResult:
    """KPI-4 — 동일 건 연속 처리: 2개 이상 변환 출력 묶음을 검증한다."""
    errors: list[str] = []
    if len(output_groups) < min_groups:
        errors.append(
            f"session: expected at least {min_groups} conversion outputs, got {len(output_groups)}"
        )
    for i, group in enumerate(output_groups, start=1):
        group_errors = _collect_errors(
            group,
            profile=profile,
            source_value=source_value,
            source_unit=source_unit,
            expected_targets=expected_targets,
        )
        errors.extend(f"group {i}: {e}" for e in group_errors)
    return _to_result(errors)
