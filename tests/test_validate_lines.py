"""PRD §1.4 KPI — validate_lines RED/GREEN 테스트 골격.

| KPI | 테스트 | 모듈 |
|-----|--------|------|
| KPI-4 | test_kpi4_* | validate_session |
| KPI-5 | test_kpi5_* | validate_lines (profile) |
| KPI-6 | test_kpi6_* | validate_lines (default, 3단위) |

KPI-1·2: 실무/E2E (범위 밖) · KPI-3: tests/entity/
"""

from src.validate_lines import validate_lines, validate_session


# --- KPI-6: 기본 3단위 변환 (FR-02/03/07, NFR-01) ---


def test_kpi6_default_meter_feet_yard_pass():
    # Arrange
    lines = [
        "2.5 meter = 8.2021 feet",
        "2.5 meter = 2.7340 yard",
    ]
    # Act
    result = validate_lines(lines, profile="default")
    # Assert
    assert result == {"status": "pass", "failed_lines": []}


# --- KPI-5: 출력 포맷 (FR-10/12) ---


def test_kpi5_business_meter_two_decimals_mm_integer_pass():
    # Arrange
    lines = [
        "2.5 meter = 8.2021 feet",
        "2.5 meter = 2.7340 yard",
        "2.5 meter = 98.4252 inch",
        "2.5 meter = 2500 mm",
    ]
    # Act
    result = validate_lines(lines, profile="business")
    # Assert
    assert result == {"status": "pass", "failed_lines": []}


def test_kpi5_business_missing_mm_incomplete():
    # Arrange
    lines = [
        "2.5 meter = 8.2021 feet",
        "2.5 meter = 2.7340 yard",
    ]
    # Act
    result = validate_lines(lines, profile="business")
    # Assert
    assert result == {
        "status": "incomplete",
        "failed_lines": ["missing target units: inch, mm"],
    }


# --- KPI-4: 연속 처리 (FR-11, validate_session) ---


def test_kpi4_session_two_groups_pass():
    # Arrange
    groups = [
        [
            "2.5 meter = 8.2021 feet",
            "2.5 meter = 2.7340 yard",
        ],
        [
            "3 meter = 9.8425 feet",
            "3 meter = 3.2808 yard",
        ],
    ]
    # Act
    result = validate_session(groups, profile="default", min_groups=2)
    # Assert
    assert result == {"status": "pass", "failed_lines": []}
