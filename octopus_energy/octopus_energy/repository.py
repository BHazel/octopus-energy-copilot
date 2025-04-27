"""
A repository for working with data from the Octopus Energy API.
"""

from datetime import datetime
from .client import OctopusEnergyClientBase
from .model import (
    Account,
    Consumption,
    ConsumptionGrouping,
    Product,
    ProductFiltering
)

class OctopusEnergyRepository:
    """
    A repository for working with data from the Octopus Energy API.
    """

    def __init__(self, client: OctopusEnergyClientBase):
        """
        Initializes an instance of the OctopusEnergyRepository class.

        Args:
            client (OctopusEnergyClientBase): The Octopus Energy client.
        """
        self.client: OctopusEnergyClientBase = client

    def get_account(self) -> Account:
        """
        Gets an account.

        Returns:
            Account: The account.
        """
        return self.client.get_account()

    def get_consumption(self,
                        from_date: datetime = None,
                        to_date: datetime = None,
                        grouping: ConsumptionGrouping = 'half-hour'
        ) -> list[Consumption]:
        """
        Gets consumption data in set intervals between two dates.

        Args:
            from_date (datetime, optional): The start date for the consumption data.
                Defaults to None.
            to_date (datetime, optional): The end date for the consumption data.
                Defaults to None.
            grouping (ConsumptionGrouping, optional): The grouping of the consumption data.
                Defaults to 'half-hour'.

        Returns:
            list[Consumption]: A list of consumption data.
        """
        return self.client.get_consumption(from_date, to_date, grouping)

    def get_max_consumption(self,
                            from_date: datetime = None,
                            to_date: datetime = None,
                            grouping: ConsumptionGrouping = 'half-hour'
        ) -> Consumption:
        """
        Gets the period with maximum consumption between two dates.

        Args:
            from_date (datetime, optional): The start date for the consumption data.
                Defaults to None.
            to_date (datetime, optional): The end date for the consumption data.
                Defaults to None.
            grouping (ConsumptionGrouping, optional): The grouping of the consumption data.
                Defaults to 'half-hour'.

        Returns:
            Consumption: The period with maximum consumption.
        """
        consumption_data: list[Consumption] = self.get_consumption(from_date, to_date, grouping)
        max_consumption = max(consumption_data, key=lambda c: c.consumption)
        return max_consumption

    def get_min_consumption(self,
                            from_date: datetime = None,
                            to_date: datetime = None,
                            grouping: ConsumptionGrouping = 'half-hour'
        ) -> Consumption:
        """
        Gets the period with minimum consumption between two dates.

        Args:
            from_date (datetime, optional): The start date for the consumption data.
                Defaults to None.
            to_date (datetime, optional): The end date for the consumption data.
                Defaults to None.
            grouping (ConsumptionGrouping, optional): The grouping of the consumption data.
                Defaults to 'half-hour'.

        Returns:
            Consumption: The period with minimum consumption.
        """
        consumption_data: list[Consumption] = self.get_consumption(from_date, to_date, grouping)
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
        consumption = Consumption(total_consumption, interval_start.isoformat(), interval_end.isoformat())
        return consumption

    def get_products(self,
                     availability_date: datetime = None,
                     filtering: ProductFiltering = ProductFiltering.DEFAULT
        ) -> list[Product]:
        """
        Gets all products.

        Args:
            availability_date (datetime, optional): The date to filter products by availability.
                Defaults to None.
            filtering (ProductFiltering, optional): The filtering of the products.
                Defaults to ProductFiltering.DEFAULT.
        """
        return self.client.get_products(availability_date, filtering)
