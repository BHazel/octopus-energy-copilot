"""
AI tools for working with consumption data.
"""

from datetime import datetime, timedelta
import jsonpickle
from dotenv import load_dotenv
from langchain_core.tools import tool
from .. import OCTOPUS_ENERGY_REPOSITORY

load_dotenv()

@tool
def get_max_consumption(from_date: str = None,
                        to_date: str = None,
                        period: str = 'half-hour'
    ) -> str:
    """
    Gets the data for the period of maximum consumption as a JSON object,
    containing the consumption in kWh and the start and end dates, from the Octopus
    Energy API.  By default the period is 30 minutes, provided as 'half-hour', but
    other possibilities include an hour ('hour'), a day ('day'), a week ('week'),
    a month ('month') and a quarter ('quarter').

    Args:
        from_date: The start date for the period in ISO-8601 format excluding time zone information.
        to_date: The end date for the period in ISO-8601 format excluding time zone information.
        period: The period of time to group the consumption data by.
            Possible Values: 'half-hour', 'hour', 'day', 'week', 'month', 'quarter'.

    Returns:
        str: The consumption data for the period of maximum consumption
        as a JSON object, including the consumption value in kWh and the start and
        end date and times of the period.
    """
    start_date = datetime.fromisoformat(from_date) if from_date else None
    end_date = datetime.fromisoformat(to_date) if to_date else None

    max_consumption = OCTOPUS_ENERGY_REPOSITORY.get_max_consumption(start_date, end_date, period)
    return jsonpickle.encode(max_consumption)

@tool
def get_min_consumption(from_date: str = None,
                        to_date: str = None,
                        period: str = 'half-hour'
    ) -> str:
    """
    Gets the data for the period of minimum consumption as a JSON object,
    containing the consumption in kWh and the start and end dates, from the Octopus
    Energy API.  By default the period is 30 minutes, provided as 'half-hour', but
    other possibilities include an hour ('hour'), a day ('day'), a week ('week'),
    a month ('month') and a quarter ('quarter').

    Args:
        from_date: The start date for the period in ISO-8601 format excluding time zone information.
        to_date: The end date for the period in ISO-8601 format excluding time zone information.
        period: The period of time to group the consumption data by.
            Possible Values: 'half-hour', 'hour', 'day', 'week', 'month', 'quarter'.

    Returns:
        str: The consumption data for the period of minimum consumption
        as a JSON object, including the consumption value in kWh and the start and
        end date and times of the period.
    """
    start_date = datetime.fromisoformat(from_date) if from_date else None
    end_date = datetime.fromisoformat(to_date) if to_date else None

    min_consumption = OCTOPUS_ENERGY_REPOSITORY.get_min_consumption(start_date, end_date, period)
    return jsonpickle.encode(min_consumption)

@tool
def get_total_consumption(from_date: str = None,
                          to_date: str = None
    ) -> str:
    """
    Gets the total consumption for a given period from the Octopus Energy API as a JSON object,
    containing the consumption in kWh and the start and end dates, from the Octopus Energy API.

    Args:
        from_date: The start date for the period in ISO-8601 format excluding time zone information.
        to_date: The end date for the period in ISO-8601 format excluding time zone information.

    Returns:
        str: The total consumption data for the given period as a JSON object
            including the consumption value in kWh and the start and end date
            and times of the period.
    """
    start_date = datetime.fromisoformat(from_date) if from_date else None
    end_date = datetime.fromisoformat(to_date) if to_date else None

    total_consumption = OCTOPUS_ENERGY_REPOSITORY.get_total_consumption(start_date, end_date)
    return jsonpickle.encode(total_consumption)

@tool
def get_period_for_grouping(from_date: str = None,
                            period: str = 'half-hour') -> str:
    """
    Gets the end date and time for a period given its start date and time.
    By default the period is 30 minutes, provided as 'half-hour', but
    other possibilities include an hour ('hour'), a day ('day'), a week ('week'),
    a month ('month') and a quarter ('quarter').

    Args:
        from_date: The start date for the period in ISO-8601 format excluding time zone information.
        period: The period of time to group the consumption data by.
            Possible Values: 'half-hour', 'hour', 'day', 'week', 'month', 'quarter'.
    
    Returns:
        str: The date and time fo the end of the period in ISO-8601 format excluding time zone
        information.
    """
    start_date = datetime.fromisoformat(from_date) if from_date else None
    match period:
        case 'half-hour':
            end_date = start_date + timedelta(minutes=30)
        case 'hour':
            end_date = start_date + timedelta(hours=1)
        case 'day':
            end_date = start_date + timedelta(days=1)
        case 'week':
            end_date = start_date + timedelta(weeks=1)
        case 'month':
            end_date = start_date + timedelta(days=30)
        case 'quarter':
            end_date = start_date + timedelta(days=90)
        case _:
            end_date = start_date

    return end_date.isoformat()
