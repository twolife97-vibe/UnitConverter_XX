"""PRD §1.4 KPI-4 — session/continuous.run_continuous RED/GREEN.

| KPI | 테스트 | 모듈 |
|-----|--------|------|
| KPI-4 | test_kpi4_* | run_continuous (FR-11) |
"""

from src.input.entity.d_loc_01 import parse_unit_value_coords
from src.output.text import convert_to_lines
from src.session.continuous import run_continuous


def _cli_convert(raw: str) -> list[str]:
    parsed = parse_unit_value_coords(raw)
    if parsed["status"] != "ok":
        return []
    return convert_to_lines(parsed["value"], parsed["unit"], profile="default")


def test_kpi4_run_continuous_two_inputs_pass(monkeypatch):
    # Arrange — meter:2.5 → yard:3 → quit (KPI-4: 동일 세션 2+ 입력)
    responses = iter(["meter:2.5", "yard:3", "quit"])
    monkeypatch.setattr("builtins.input", lambda _prompt="": next(responses))

    # Act
    groups = run_continuous(convert_fn=_cli_convert, min_inputs=2)

    # Assert
    assert len(groups) == 2
    assert groups[0] == [
        "2.5 meter = 8.2021 feet",
        "2.5 meter = 2.7340 yard",
    ]
    assert groups[1] == [
        "3 yard = 9.0000 feet",
    ]
