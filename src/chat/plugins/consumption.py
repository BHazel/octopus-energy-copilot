"""
AI tools for working with consumption data.
"""

import os
from datetime import datetime, timedelta
from typing import Annotated
import jsonpickle
from dotenv import load_dotenv
from semantic_kernel.functions import kernel_function
from octopus_energy.client import OctopusEnergyClient
from octopus_energy.model import ConsumptionGrouping
from octopus_energy.repository import OctopusEnergyRepository

load_dotenv()

class ConsumptionPlugin:
    """
    AI plug-in for working with consumption data.
    """

    def __init__(self):
        """
        Initialises an instance of the ConsumptionPlugin class.
        """
        self.repository = OctopusEnergyRepository(
            OctopusEnergyClient(
                os.environ['OCTOPUS_ENERGY_API_KEY'],
                None,
                os.environ['OCTOPUS_ENERGY_METER_MPAN'],
                os.environ['OCTOPUS_ENERGY_METER_SERIAL']))

    @kernel_function(name='get_max_consumption',
                     description="""
                        Gets the data for the period of maximum consumption as a JSON object,
                        containing the consumption in kWh and the start and end dates in ISO-8601 format,
                        from the Octopus Energy API.  By default the period is 30 minutes, provided as
                        'half-hour', but other possibilities include an hour ('hour'), a day ('day'),
                        a week ('week'), a month ('month') and a quarter ('quarter').
                     """)
    def get_max_consumption(self,
                            from_date: str = None,
                            to_date: str = None,
                            period: str = 'half-hour'
        ) -> Annotated[str, """
                        The consumption data for the period of maximum consumption
                        as a JSON object, including the consumption value in kWh and the start and
                        end date and times of the period.
                    """]:
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
        period = ConsumptionGrouping(None if period == 'half-hour' else period)

        max_consumption = self.repository.get_max_consumption(start_date, end_date, period)
        return jsonpickle.encode(max_consumption)

    @kernel_function(name='get_min_consumption',
                    description="""
                        Gets the data for the period of minimum consumption as a JSON object,
                        containing the consumption in kWh and the start and end dates in ISO-8601 format,
                        from the Octopus Energy API.  By default the period is 30 minutes, provided as
                        'half-hour', but other possibilities include an hour ('hour'), a day ('day'),
                        a week ('week'), a month ('month') and a quarter ('quarter').
                    """)
    def get_min_consumption(self,
                            from_date: str = None,
                            to_date: str = None,
                            period: str = 'half-hour'
        ) -> Annotated[str, """
                        The consumption data for the period of minimum consumption
                        as a JSON object, including the consumption value in kWh and the start and
                        end date and times of the period.
                    """]:
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

        min_consumption = self.repository.get_min_consumption(start_date, end_date, period)
        return jsonpickle.encode(min_consumption)

    @kernel_function(name='get_total_consumption',
                    description="""
                        Gets the total consumption for a given period from the Octopus Energy API as a JSON object,
                        containing the consumption in kWh and the start and end dates in ISO-8601 format, from the
                        Octopus Energy API.
                    """)
    def get_total_consumption(self,
                              from_date: str = None,
                              to_date: str = None
        ) -> Annotated[str, """
                            The total consumption data for the given period as a JSON object
                            including the consumption value in kWh and the start and end date
                            and times of the period.
                            """]:
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

        total_consumption = self.repository.get_total_consumption(start_date, end_date)
        return jsonpickle.encode(total_consumption)

    @kernel_function(name='get_period_for_grouping',
                    description="""
                        Gets the end date and time in ISO-8601 format for a period given its
                        start date and time.  By default the period is 30 minutes, provided as 'half-hour',
                        but other possibilities include an hour ('hour'), a day ('day'), a week ('week'),
                        a month ('month') and a quarter ('quarter').
                    """)
    def get_period_for_grouping(self,
                                from_date: str = None,
                                period: str = 'half-hour'
        ) -> Annotated[str, """
                    The date and time fo the end of the period in ISO-8601 format excluding time zone
                    information.
                    """]:
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
        grouping = ConsumptionGrouping(period)
        start_date = datetime.fromisoformat(from_date) if from_date else None
        match grouping:
            case ConsumptionGrouping.HALF_HOUR:
                end_date = start_date + timedelta(minutes=30)
            case ConsumptionGrouping.HOUR:
                end_date = start_date + timedelta(hours=1)
            case ConsumptionGrouping.DAY:
                end_date = start_date + timedelta(days=1)
            case ConsumptionGrouping.WEEK:
                end_date = start_date + timedelta(weeks=1)
            case ConsumptionGrouping.MONTH:
                end_date = start_date + timedelta(days=30)
            case ConsumptionGrouping.QUARTER:
                end_date = start_date + timedelta(days=90)
            case _:
                end_date = start_date

        return end_date.isoformat()
