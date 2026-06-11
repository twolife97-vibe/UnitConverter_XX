"""변환 CLI 출력 형식 계약.

프로필:
- default: 기본 2줄 (feet, yard), 소수 4자리
- business: STEP2 성공 #5 — meter 소수 2자리, mm 정수, inch/mm 포함 전 타깃

예 (business, meter:2.5):
    2.5 meter = 8.2021 feet
    2.5 meter = 2.7340 yard
    2.5 meter = 98.4252 inch
    2.5 meter = 2500 mm
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

Profile = Literal["default", "business"]

RATIOS_TO_METER = {
    "meter": 1.0,
    "feet": 3.28084,
    "yard": 1.09361,
    "inch": 39.37007874015748,
    "mm": 1000.0,
}
SUPPORTED_UNITS = frozenset(RATIOS_TO_METER)

DISPLAY_DECIMALS: dict[Profile, dict[str, int]] = {
    "default": {
        "meter": 4,
        "feet": 4,
        "yard": 4,
        "inch": 4,
        "mm": 4,
    },
    "business": {
        "meter": 2,
        "feet": 4,
        "yard": 4,
        "inch": 4,
        "mm": 0,
    },
}

DEFAULT_TARGETS: dict[Profile, frozenset[str]] = {
    "default": frozenset({"feet", "yard"}),
    "business": SUPPORTED_UNITS,
}

LINE_RE = re.compile(
    r"^(?P<src_val>\S+)\s+(?P<src_unit>\S+)\s+=\s+(?P<dst_val>\S+)\s+(?P<dst_unit>\S+)$"
)


@dataclass(frozen=True)
class ParsedLine:
    src_val: float
    src_unit: str
    dst_val: float
    dst_unit: str
    raw_dst_val: str


def _to_meters(value: float, unit: str) -> float:
    return value / RATIOS_TO_METER[unit]


def _from_meters(meters: float, unit: str) -> float:
    return meters * RATIOS_TO_METER[unit]


def _tolerance_for(unit: str, profile: Profile) -> float:
    decimals = DISPLAY_DECIMALS[profile][unit]
    if decimals == 0:
        return 0.5
    return 0.5 * 10 ** (-decimals)


def format_converted(value: float, unit: str, profile: Profile = "default") -> str:
    decimals = DISPLAY_DECIMALS[profile][unit]
    if decimals == 0:
        return str(int(round(value)))
    return f"{value:.{decimals}f}"


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


def validate_lines(
    lines: list[str],
    *,
    source_value: float | None = None,
    source_unit: str | None = None,
    profile: Profile = "default",
    expected_targets: frozenset[str] | set[str] | None = None,
) -> list[str]:
    """변환 출력 줄 목록을 검증한다. 위반 메시지 목록을 반환 (빈 리스트 = 통과)."""
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
            _from_meters(_to_meters(p.src_val, p.src_unit), p.dst_unit),
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


def validate_session(
    output_groups: list[list[str]],
    *,
    min_groups: int = 2,
    profile: Profile = "business",
    source_value: float | None = None,
    source_unit: str | None = None,
    expected_targets: frozenset[str] | set[str] | None = None,
) -> list[str]:
    """동일 건 연속 처리(성공 #4): 2개 이상 변환 출력 묶음을 검증한다."""
    errors: list[str] = []
    if len(output_groups) < min_groups:
        errors.append(
            f"session: expected at least {min_groups} conversion outputs, got {len(output_groups)}"
        )
    for i, group in enumerate(output_groups, start=1):
        group_errors = validate_lines(
            group,
            profile=profile,
            source_value=source_value,
            source_unit=source_unit,
            expected_targets=expected_targets,
        )
        errors.extend(f"group {i}: {e}" for e in group_errors)
    return errors
