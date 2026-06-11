"""KPI-5 — default / business 출력 프로필 (PRD §1.4, STEP3)."""

from typing import Literal

from src.registry.units import SUPPORTED_UNITS

Profile = Literal["default", "business"]

DISPLAY_DECIMALS: dict[Profile, dict[str, int]] = {
    "default": {
        "meter": 4,
        "feet": 4,
        "yard": 4,
        "inch": 4,
        "mm": 4,
    },
    "business": {
        "meter": 2,
        "feet": 4,
        "yard": 4,
        "inch": 4,
        "mm": 0,
    },
}

DEFAULT_TARGETS: dict[Profile, frozenset[str]] = {
    "default": frozenset({"feet", "yard"}),
    "business": SUPPORTED_UNITS,
}

TARGET_ORDER: dict[Profile, tuple[str, ...]] = {
    "default": ("feet", "yard"),
    "business": ("feet", "yard", "inch", "mm"),
}
