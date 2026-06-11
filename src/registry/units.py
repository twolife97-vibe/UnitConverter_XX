"""KPI-6 · FR-03 · NFR-01 — meter 기준 단위 비율 (PRD §3·§6.2)."""

RATIOS_TO_METER = {
    "meter": 1.0,
    "feet": 3.28084,
    "yard": 1.09361,
    "inch": 39.37007874015748,
    "mm": 1000.0,
}

BASE_UNITS_V1 = frozenset({"meter", "feet", "yard"})
SUPPORTED_UNITS = frozenset(RATIOS_TO_METER)
