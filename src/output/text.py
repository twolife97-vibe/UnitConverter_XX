"""KPI-5 · FR-02/10/12 — 프로필별 변환 출력 줄 생성 (GREEN 대상)."""

from src.registry.profiles import DEFAULT_TARGETS, Profile


def convert_to_lines(
    value: float,
    unit: str,
    *,
    profile: Profile = "default",
) -> list[str]:
    """입력 단위·값을 프로필별 변환 출력 줄 목록으로 반환한다."""
    raise NotImplementedError(
        "GREEN: output/text.convert_to_lines — "
        f"profile={profile!r}, targets={DEFAULT_TARGETS[profile]}"
    )
