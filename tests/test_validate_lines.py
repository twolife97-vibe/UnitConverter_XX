from src.validate_lines import validate_lines


def test_business_meter_pass():
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
