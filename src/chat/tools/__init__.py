"""
AI tools module.
"""

from chat.tools.account import get_account
from chat.tools.consumption import (
    get_max_consumption,
    get_min_consumption,
    get_period_for_grouping,
    get_total_consumption
)
from chat.tools.conversion import (
    calculate_energy,
    calculate_power,
    convert_energy,
    convert_energy_to_co2,
    convert_power
)

def tools() -> dict[str, callable]:
    """
    Returns:
        dict[str, callable]: The tools available to the AI copilot.
    """
    return {
        'calculate_energy': calculate_energy,
        'calculate_power': calculate_power,
        'convert_energy': convert_energy,
        'convert_energy_to_co2': convert_energy_to_co2,
        'convert_power': convert_power,
        'get_account': get_account,
        'get_max_consumption': get_max_consumption,
        'get_min_consumption': get_min_consumption,
        'get_period_for_grouping': get_period_for_grouping,
        'get_total_consumption': get_total_consumption
    }
