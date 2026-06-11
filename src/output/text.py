"""KPI-5 · FR-02/10/12 — 프로필별 변환 출력 줄 생성 (GREEN 대상)."""

from src.conversion.meter import convert, format_converted
from src.registry.profiles import DEFAULT_TARGETS, TARGET_ORDER, Profile


def convert_to_lines(
    value: float,
    unit: str,
    *,
    profile: Profile = "default",
) -> list[str]:
    """입력 단위·값을 프로필별 변환 출력 줄 목록으로 반환한다."""
    targets = DEFAULT_TARGETS[profile] - {unit}
    src = f"{value:g}"
    return [
        f"{src} {unit} = {format_converted(convert(value, unit, target), target, profile)} {target}"
        for target in TARGET_ORDER[profile]
        if target in targets
    ]
