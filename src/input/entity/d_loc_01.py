def parse_unit_value_coords(raw: str) -> dict:
    if ":" not in raw:
        return {
            "status": "invalid",
            "unit": None,
            "value": None,
            "errors": ["Invalid format. Use unit:value (ex: meter:2.5)"],
        }
    unit, value_str = raw.split(":", 1)
    try:
        value = float(value_str)
    except ValueError:
        return {
            "status": "invalid",
            "unit": unit,
            "value": None,
            "errors": [f"Invalid number: {value_str}"],
        }
    return {
        "status": "ok",
        "unit": unit,
        "value": value,
        "errors": [],
    }
