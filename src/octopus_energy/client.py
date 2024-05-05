"""
A client and types for interacting with the Octopus Energy API.
"""

import json
from datetime import datetime
from requests import get, Response
from octopus_energy.model import Consumption

BASE_URI: str = 'https://api.octopus.energy/v1'

class ConsumptionResponse:
    """
    Represents a response from the Octopus Energy API containing consumption data.
    """

    def __init__(self, count: int, next: str, previous: str, results: list[Consumption]):
        """
        Represents a response from the Octopus Energy API containing consumption data split into
        30-minute periods.

        Args:
            count (int): The count of consumption data entries in the response.
            next (str): The URL for the next page of consumption data if available, otherwise None.
            previous (str): The URL for the previous page of consumption data if available,
                otherwise None.
            results (list[Consumption]): The consumption data entries.
        """
        self.count: int = count
        self.next: str = next
        self.previous: str = previous
        self.results: list[Consumption] = results

class OctopusEnergyClient:
    """
    A client for interacting with the Octopus Energy API.
    """

    def __init__(self, api_key: str, meter_mpan: str, meter_serial: str):
        """
        Initializes an instance of the OctopusEnergyClient class.

        Args:
            apiKey (str): The API key for accessing the Octopus Energy API.
            meter_mpan (str): The Meter Point Administration Number (MPAN) for the meter.
            meter_serial (str): The serial number for the meter.
        """
        self.api_key: str = api_key
        self.meter_mpan: str = meter_mpan
        self.meter_serial: str = meter_serial

    def get_consumption(self,
                        from_date: datetime = None,
                        to_date: datetime = None
        ) -> list[Consumption]:
        """
        Retrieves consumption data from the Octopus Energy API.

        Args:
            from_date (datetime, optional): The start date for the consumption data.
                Defaults to None.
            to_date (datetime, optional): The end date for the consumption data.
                Defaults to None.

        Returns:
            list[Consumption]: A list of consumption data.
        """
        consumption_data: list[Consumption] = []
        is_next: bool = True
        page: int = 1
        while is_next:
            consumption: ConsumptionResponse = self.get_consumption_page(from_date, to_date, page)
            consumption_data += consumption.results
            page += 1
            if consumption.next is None:
                is_next = False

        return consumption_data

    def get_consumption_page(self,
                             from_date: datetime = None,
                             to_date: datetime = None,
                             page: int = 1
        ) -> ConsumptionResponse:
        """
        Retrieves a specific page of consumption data from the Octopus Energy API.

        Args:
            from_date (datetime, optional): The start date and time for the consumption data.
                Defaults to None.
            to_date (datetime, optional): The end date for the consumption data.
                Defaults to None.
            page (int, optional): The page number of the consumption data.
                Defaults to 1.

        Returns:
            ConsumptionResponse: The specified page of consumption data.
        """
        base_request_uri: str = f'{BASE_URI}/electricity-meter-points/{self.meter_mpan}/meters/{self.meter_serial}/consumption'
        parameters: dict[str, str] = {}
        if from_date:
            parameters['period_from'] = from_date.isoformat()
        if to_date:
            parameters['period_to'] = to_date.isoformat()
        if page:
            parameters['page'] = page

        url_parameters: str = ''
        if len(parameters) > 0:
            url_parameters = f'?{'&'.join([f'{key}={value}' for key, value in parameters.items()])}'

        response: Response = self.get(f'{base_request_uri}{url_parameters}')

        consumption_data = json.loads(response.text)
        results_data = consumption_data['results']
        results = [Consumption(**result_entry) for result_entry in results_data]

        consumption: ConsumptionResponse = ConsumptionResponse(
            consumption_data['count'],
            consumption_data['next'],
            consumption_data['previous'],
            results)

        return consumption

    def get(self, url) -> Response:
        """
        Sends an HTTP GET request to the specified URL.

        It is configured with authorisation for the Octopus Energy API and a default timeout of
        10 seconds.

        Args:
            url (str): The URL to send the request to.

        Returns:
            Response: The response from the URL.
        """
        return get(url=url, auth=(self.api_key, ''), timeout=10)
