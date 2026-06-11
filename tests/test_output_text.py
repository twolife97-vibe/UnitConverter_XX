"""PRD §1.4 KPI-5/6 — output/text.convert_to_lines RED/GREEN.

| KPI | 테스트 | 모듈 |
|-----|--------|------|
| KPI-6 | test_kpi6_* | convert_to_lines(profile=default) |
| KPI-5 | test_kpi5_* | convert_to_lines(profile=business) |
"""

from src.output.text import convert_to_lines


# --- KPI-6: 기본 3단위 변환 (FR-02/03/07, NFR-01) ---


def test_kpi6_convert_to_lines_default_pass():
    # Arrange
    value, unit = 2.5, "meter"
    # Act
    lines = convert_to_lines(value, unit, profile="default")
    # Assert
    assert lines == [
        "2.5 meter = 8.2021 feet",
        "2.5 meter = 2.7340 yard",
    ]


def test_kpi6_convert_validates_three_base_units():
    # Arrange/Act/Assert — FR-07: meter/feet/yard 출력 → validate_lines pass
    from src.validate_lines import validate_lines

    cases = [(2.5, "meter"), (12, "feet"), (2.5, "yard")]
    for value, unit in cases:
        lines = convert_to_lines(value, unit, profile="default")
        result = validate_lines(lines, profile="default")
        assert result == {"status": "pass", "failed_lines": []}


# --- KPI-5: 출력 포맷 (FR-10/12) — business ---


def test_kpi5_convert_to_lines_business_pass():
    # Arrange
    value, unit = 2.5, "meter"
    # Act
    lines = convert_to_lines(value, unit, profile="business")
    # Assert
    assert lines == [
        "2.5 meter = 8.2021 feet",
        "2.5 meter = 2.7340 yard",
        "2.5 meter = 98.4252 inch",
        "2.5 meter = 2500 mm",
    ]


# --- Golden Master (PRD §3 · STEP3) ---


def test_golden_g3_feet_default():
    # Arrange — G3: feet:12 · default · 타깃 yard만
    value, unit = 12, "feet"
    # Act
    lines = convert_to_lines(value, unit, profile="default")
    # Assert
    assert lines == [
        "12 feet = 4.0000 yard",
    ]


def test_golden_g4_yard_default():
    # Arrange — G4: yard:2.5 · default · 타깃 feet만
    value, unit = 2.5, "yard"
    # Act
    lines = convert_to_lines(value, unit, profile="default")
    # Assert
    assert lines == [
        "2.5 yard = 7.5000 feet",
    ]


def test_golden_g5_meter_business():
    # Arrange — G5: meter:1 · business · mm 정수 1000
    value, unit = 1, "meter"
    # Act
    lines = convert_to_lines(value, unit, profile="business")
    # Assert
    assert lines == [
        "1 meter = 3.2808 feet",
        "1 meter = 1.0936 yard",
        "1 meter = 39.3701 inch",
        "1 meter = 1000 mm",
    ]
