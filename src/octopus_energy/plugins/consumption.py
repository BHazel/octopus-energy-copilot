from datetime import datetime
from typing import Annotated
from dotenv import load_dotenv
import jsonpickle
from semantic_kernel.functions.kernel_function_decorator import kernel_function
from octopus_energy.client import OctopusEnergyClient

load_dotenv()

class ConsumptionPlugin:
    def __init__(self, api_key: str, meter_mpan: str, meter_serial: str):
        """
        Initializes a new instance of the ConsumptionPlugin class.
        """
        self.octopus_energy_client = OctopusEnergyClient(
            api_key,
            meter_mpan,
            meter_serial)

    @kernel_function(
            description='Gets the data for the period of maximum consumption, containing the consumption in kWh and the start and end dates, from the Octopus Energy API.',
            name='GetMaxConsumption')
    def get_max_consumption(self):
        """
        Gets the data for the period of maximum consumption from the Octopus Energy API.

        Returns:
            str: A JSON object of consumption data for the period of maximum consumption.
        """
        consumption = self.octopus_energy_client.get_consumption()
        max_consumption = max(consumption, key=lambda x: x.consumption)
        return jsonpickle.encode(max_consumption)
    
    @kernel_function(
            description='Gets the total consumption between two dates, containing the consumption in kWh and the start and end dates, from the Octopus Energy API.',
            name='GetTotalConsumption')
    def get_total_consumption(self,
                              from_date: Annotated[str, 'The date and time in ISO-8601 format to start retrieving consumption from.'],
                              to_date: Annotated[str, 'The date and time in ISO-8601 format to stop retrieving consumption from.']
        ):
        """
        Gets the total consumption between two dates from the Octopus Energy API.

        Args:
            from_date (str, optional): The start date for the consumption data in ISO-8601 format.
            to_date (str, optional): The end date for the consumption data in ISO-8601 format.

        Returns:
            str: A JSON string of the total consumption value in kWh between two dates.
        """
        start_date = datetime.fromisoformat(from_date)
        end_date = datetime.fromisoformat(to_date)
        consumption = self.octopus_energy_client.get_consumption(start_date, end_date)
        total_consumption = sum([x.consumption for x in consumption])
        return jsonpickle.encode(total_consumption)

    @kernel_function(
            description='Gets the consumption between two dates rom the Octopus Energy API as a JSON collection in 30-minute periods each containing the consumption in kWh and the start and end dates.',
            name='GetConsumptionForPeriod'
    )
    def get_consumption_for_period(self,
                                   from_date: Annotated[str, 'The start date and time in ISO-8601 format.'],
                                   to_date: Annotated[str, 'The end date and time in ISO-8601 format.']
        ):
        """
        Gets consumption data between two dates from the Octopus Energy API.

        Args:
            from_date (str, optional): The start date for the consumption data in ISO-8601 format.
            to_date (str, optional): The end date for the consumption data in ISO-8601 format.

        Returns:
            str: A JSON array of consumption data, each containing the start and end dates and the consumption in kWh.
        """
        start_date = datetime.fromisoformat(from_date)
        end_date = datetime.fromisoformat(to_date)
        consumption = self.octopus_energy_client.get_consumption(start_date, end_date)
        return jsonpickle.encode(consumption)
