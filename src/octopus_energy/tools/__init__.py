"""
AI tools module.
"""

from octopus_energy.tools.consumption import (
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
        'get_max_consumption': get_max_consumption,
        'get_min_consumption': get_min_consumption,
        'get_period_for_grouping': get_period_for_grouping,
        'get_total_consumption': get_total_consumption
    }
