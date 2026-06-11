"""KPI-4 · FR-11 — 동일 세션 연속 입력 (GREEN 대상).

KPI-1(재발주 0건)·KPI-2(≤20분)는 실무·E2E 측정 — 코드 계약 범위 밖.
"""

from collections.abc import Callable


def run_continuous(
    convert_fn: Callable[[str], list[str]] | None = None,
    *,
    min_inputs: int = 2,
) -> list[list[str]]:
    """quit/exit 전까지 다중 unit:value 입력 → 출력 줄 묶음 목록."""
    raise NotImplementedError(
        "GREEN: session/continuous.run_continuous — "
        f"min_inputs={min_inputs}"
    )
