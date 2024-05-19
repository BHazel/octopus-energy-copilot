"""
AI tools for working with consumption data.
"""

import os
from datetime import datetime
import jsonpickle
from dotenv import load_dotenv
from langchain_core.tools import tool
from octopus_energy.client import OctopusEnergyClient
from octopus_energy.repository import OctopusEnergyRepository

load_dotenv()

repository = OctopusEnergyRepository(
    OctopusEnergyClient(
        os.environ['OCTOPUS_ENERGY_API_KEY'],
        os.environ['OCTOPUS_ENERGY_METER_MPAN'],
        os.environ['OCTOPUS_ENERGY_METER_SERIAL']))

@tool
def get_max_consumption(from_date: str = None,
                        to_date: str = None
    ) -> str:
    """
    Gets the data for the 30 minute period of maximum consumption as a JSON object,
    containing the consumption in kWh and the start and end dates, from the Octopus
    Energy API.

    Args:
        from_date: The start date for the period in ISO-8601 format excluding time zone information.
        to_date: The end date for the period in ISO-8601 format excluding time zone information.

    Returns:
        str: The consumption data for the 30-minute period of maximum consumption
        as a JSON object, including the consumption value in kWh and the start and
        end date and times of the period.
    """
    start_date = datetime.fromisoformat(from_date) if from_date else None
    end_date = datetime.fromisoformat(to_date) if to_date else None

    max_consumption = repository.get_max_consumption(start_date, end_date)
    return jsonpickle.encode(max_consumption)

@tool
def get_min_consumption(from_date: str = None,
                        to_date: str = None
    ) -> str:
    """
    Gets the data for the 30 minute period of minimum consumption as a JSON object,
    containing the consumption in kWh and the start and end dates, from the Octopus
    Energy API.

    Args:
        from_date: The start date for the period in ISO-8601 format excluding time zone information.
        to_date: The end date for the period in ISO-8601 format excluding time zone information.

    Returns:
        str: The consumption data for the 30-minute period of minimum consumption
        as a JSON object, including the consumption value in kWh and the start and
        end date and times of the period.
    """
    start_date = datetime.fromisoformat(from_date) if from_date else None
    end_date = datetime.fromisoformat(to_date) if to_date else None

    min_consumption = repository.get_min_consumption(start_date, end_date)
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

    total_consumption = repository.get_total_consumption(start_date, end_date)
    return jsonpickle.encode(total_consumption)
