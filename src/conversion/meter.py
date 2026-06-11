"""KPI-6 · FR-03 — meter 기준 변환."""

from src.registry.profiles import DISPLAY_DECIMALS, Profile
from src.registry.units import RATIOS_TO_METER


def to_meters(value: float, unit: str) -> float:
    return value / RATIOS_TO_METER[unit]


def from_meters(meters: float, unit: str) -> float:
    return meters * RATIOS_TO_METER[unit]


def convert(value: float, from_unit: str, to_unit: str) -> float:
    return from_meters(to_meters(value, from_unit), to_unit)


def format_converted(value: float, unit: str, profile: Profile = "default") -> str:
    decimals = DISPLAY_DECIMALS[profile][unit]
    if decimals == 0:
        return str(int(round(value)))
    return f"{value:.{decimals}f}"
