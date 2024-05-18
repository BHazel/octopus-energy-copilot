"""
A repository for working with data from the Octopus Energy API.
"""

from datetime import datetime
from octopus_energy.client import OctopusEnergyClient
from octopus_energy.model import Consumption

class OctopusEnergyRepository:
    """
    A repository for working with data from the Octopus Energy API.
    """

    def __init__(self, client: OctopusEnergyClient):
        """
        Initializes an instance of the OctopusEnergyRepository class.

        Args:
            client (OctopusEnergyClient): The Octopus Energy client.
        """
        self.client: OctopusEnergyClient = client

    def get_consumption(self,
                        from_date: datetime = None,
                        to_date: datetime = None
        ) -> list[Consumption]:
        """
        Gets consumption data in 30-minute intervals between two dates.

        Args:
            from_date (datetime, optional): The start date for the consumption data.
                Defaults to None.
            to_date (datetime, optional): The end date for the consumption data.
                Defaults to None.

        Returns:
            list[Consumption]: A list of consumption data.
        """
        return self.client.get_consumption(from_date, to_date)

    def get_max_consumption(self,
                            from_date: datetime = None,
                            to_date: datetime = None
        ) -> Consumption:
        """
        Gets the 30 minute period with maximum consumption between two dates.

        Args:
            from_date (datetime, optional): The start date for the consumption data.
                Defaults to None.
            to_date (datetime, optional): The end date for the consumption data.
                Defaults to None.

        Returns:
            Consumption: The 30 minute period with maximum consumption.
        """
        consumption_data: list[Consumption] = self.get_consumption(from_date, to_date)
        max_consumption = max(consumption_data, key=lambda c: c.consumption)
        return max_consumption

    def get_min_consumption(self,
                            from_date: datetime = None,
                            to_date: datetime = None
        ) -> Consumption:
        """
        Gets the 30 minute period with minimum consumption between two dates.

        Args:
            from_date (datetime, optional): The start date for the consumption data.
                Defaults to None.
            to_date (datetime, optional): The end date for the consumption data.
                Defaults to None.

        Returns:
            Consumption: The 30 minute period with minimum consumption.
        """
        consumption_data: list[Consumption] = self.get_consumption(from_date, to_date)
        min_consumption = min(consumption_data, key=lambda c: c.consumption)
        return min_consumption

    def get_total_consumption(self,
                              from_date: datetime = None,
                              to_date: datetime = None
        ) -> Consumption:
        """
        Gets the total consumption between two dates.

        Args:
            from_date (datetime, optional): The start date for the consumption data.
                Defaults to None.
            to_date (datetime, optional): The end date for the consumption data.
                Defaults to None.

        Returns:
            Consumption: The total consumption.
        """
        consumption_data: list[Consumption] = self.get_consumption(from_date, to_date)
        total_consumption: float = sum([c.consumption for c in consumption_data])
        interval_start = from_date if from_date else min([entry.interval_start for entry in consumption_data])
        interval_end = to_date if to_date else max([entry.interval_end for entry in consumption_data])
        consumption = Consumption(total_consumption, interval_start, interval_end)
        return consumption
