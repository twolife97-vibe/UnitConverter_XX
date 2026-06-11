from src.input.entity.d_loc_01 import parse_unit_value_coords


def test_d_loc_01_blank_coords_row_major():
    # Arrange
    raw = "meter:"
    # Act
    result = parse_unit_value_coords(raw)
    # Assert
    assert result == {
        "status": "invalid",
        "unit": "meter",
        "value": None,
        "errors": ["Invalid number: "],
    }


def test_d_loc_01_valid_g1_meter(g1_valid_input):
    # Arrange — g1_valid_input fixture ("meter:2.5")
    # Act
    result = parse_unit_value_coords(g1_valid_input)
    # Assert
    assert result == {
        "status": "ok",
        "unit": "meter",
        "value": 2.5,
        "errors": [],
    }


def test_d_loc_01_missing_colon_invalid_format():
    # Arrange
    raw = "2.5"
    # Act
    result = parse_unit_value_coords(raw)
    # Assert
    assert result == {
        "status": "invalid",
        "unit": None,
        "value": None,
        "errors": ["Invalid format. Use unit:value (ex: meter:2.5)"],
    }


def test_d_loc_01_blank_unit_invalid():
    # Arrange — blank unit (PRD §4.1 후순위 RED)
    raw = ":2.5"
    # Act
    result = parse_unit_value_coords(raw)
    # Assert
    assert result == {
        "status": "invalid",
        "unit": "",
        "value": None,
        "errors": ["Invalid unit: "],
    }
