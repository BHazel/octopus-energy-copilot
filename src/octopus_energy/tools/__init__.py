"""
AI tools module.
"""

from octopus_energy.tools.account import get_account
from octopus_energy.tools.consumption import (
    convert_consumption_to_co2,
    get_max_consumption,
    get_min_consumption,
    get_period_for_grouping,
    get_total_consumption
)

def tools() -> dict[str, callable]:
    """
    Returns:
        dict[str, callable]: The tools available to the AI copilot.
    """
    return {
        'convert_consumption_to_co2': convert_consumption_to_co2,
        'get_account': get_account,
        'get_max_consumption': get_max_consumption,
        'get_min_consumption': get_min_consumption,
        'get_period_for_grouping': get_period_for_grouping,
        'get_total_consumption': get_total_consumption
    }
