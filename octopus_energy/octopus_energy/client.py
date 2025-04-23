"""
A client and types for interacting with the Octopus Energy API.
"""

from abc import ABCMeta, abstractmethod
import json
from datetime import datetime
from typing import Literal, TypeVar
from requests import get, Response
from .model import (
    Account,
    Consumption,
    ConsumptionGrouping,
    Product,
    ProductFiltering
)

BASE_URI: str = 'https://api.octopus.energy/v1'
T = TypeVar('T')
TRUE = str(True).lower()

class ClientResponse[T]:
    """
    Represents a response from the Octopus Energy API.
    """

    def __init__(self, count: int, next: str, previous: str, results: list[T]):
        """
        Initialises an instance of the ClientResponse class.

        Args:
            count (int): The count of entries in the response.
            next (str): The URL for the next page of data if available, otherwise None.
            previous (str): The URL for the previous page of data if available, otherwise None.
            results (list[T]): The data entries.
        """
        self.count: int = count
        self.next: str = next
        self.previous: str = previous
        self.results: list[T] = results

class OctopusEnergyClientBase(metaclass=ABCMeta):
    """
    Base class for clients for the Octopus Energy API.
    """
    @abstractmethod
    def get_account(self) -> Account:
        """
        Retrieves account data from the Octopus Energy API.

        Returns:
            Account: The account data.
        """

    @abstractmethod
    def get_consumption(self,
                        from_date: datetime = None,
                        to_date: datetime = None,
                        grouping: ConsumptionGrouping = ConsumptionGrouping.HALF_HOUR
        ) -> list[Consumption]:
        """
        Retrieves consumption data from the Octopus Energy API.

        Args:
            from_date (datetime, optional): The start date for the consumption data.
                Defaults to None.
            to_date (datetime, optional): The end date for the consumption data.
                Defaults to None.
            grouping (ConsumptionGrouping, optional): The grouping of the consumption data.
                Defaults to ConsumptionGrouping.HALF_HOUR.

        Returns:
            list[Consumption]: A list of consumption data.
        """

    @abstractmethod
    def get_products(self,
                     availability_date: datetime = None,
                     filtering: ProductFiltering = None
        ) -> list[Product]:
        """
        Retrieves product data from the Octopus Energy API.

        Returns:
            list[Product]: A list of product data.
        """

class OctopusEnergyClient(OctopusEnergyClientBase):
    """
    A client for interacting with the Octopus Energy API.
    """

    def __init__(self,
                 api_key: str,
                 account_number: str = None,
                 meter_mpan: str = None,
                 meter_serial: str = None
    ):
        """
        Initializes an instance of the OctopusEnergyClient class.

        Args:
            api_key (str): The API key for accessing the Octopus Energy API.
            account_number (str, optional): The Octopus Energy account number.
                Defaults to None.
            meter_mpan (str, optional): The Meter Point Administration Number (MPAN) for the meter.
                Defaults to None.
            meter_serial (str, optional): The serial number for the meter.
                Defaults to None.
        """
        self.api_key: str = api_key
        self.meter_mpan: str = meter_mpan
        self.meter_serial: str = meter_serial
        self.account_number: str = account_number

    def get_account(self) -> Account:
        """
        Retrieves account data from the Octopus Energy API.

        Returns:
            Account: The account data.
        """
        response: Response = self.get(f'{BASE_URI}/accounts/{self.account_number}')
        account_data = json.loads(response.text)
        account: Account = Account(**account_data)

        return account

    def get_consumption(self,
                        from_date: datetime = None,
                        to_date: datetime = None,
                        grouping: ConsumptionGrouping = ConsumptionGrouping.HALF_HOUR
        ) -> list[Consumption]:
        """
        Retrieves consumption data from the Octopus Energy API.

        Args:
            from_date (datetime, optional): The start date for the consumption data.
                Defaults to None.
            to_date (datetime, optional): The end date for the consumption data.
                Defaults to None.
            grouping (ConsumptionGrouping, optional): The grouping of the consumption data.
                Defaults to ConsumptionGrouping.HALF_HOUR.

        Returns:
            list[Consumption]: A list of consumption data.
        """
        consumption_data: list[Consumption] = []
        is_next: bool = True
        page: int = 1
        while is_next:
            consumption: ClientResponse = self.get_consumption_page(from_date,
                                                                    to_date,
                                                                    grouping,
                                                                    page)
            consumption_data += consumption.results
            page += 1
            if consumption.next is None:
                is_next = False

        return consumption_data

    def get_consumption_page(self,
                             from_date: datetime = None,
                             to_date: datetime = None,
                             grouping: ConsumptionGrouping = ConsumptionGrouping.HALF_HOUR,
                             page: int = 1
        ) -> ClientResponse:
        """
        Retrieves a specific page of consumption data from the Octopus Energy API.

        Args:
            from_date (datetime, optional): The start date and time for the consumption data.
                Defaults to None.
            to_date (datetime, optional): The end date for the consumption data.
                Defaults to None.
            grouping (ConsumptionGrouping, optional): The grouping of the consumption data.
                Defaults to ConsumptionGrouping.HALF_HOUR.
            page (int, optional): The page number of the consumption data.
                Defaults to 1.

        Returns:
            ClientResponse[Consumption]: The specified page of consumption data.
        """
        base_request_uri: str = f'{BASE_URI}/electricity-meter-points/{self.meter_mpan}/meters/{self.meter_serial}/consumption'
        parameters: dict[str, str] = {}
        if from_date:
            parameters['period_from'] = from_date.isoformat()
        if to_date:
            parameters['period_to'] = to_date.isoformat()
        if page:
            parameters['page'] = page
        if grouping != ConsumptionGrouping.HALF_HOUR:
            parameters['group_by'] = grouping.value

        url_parameters: str = ''
        if len(parameters) > 0:
            url_parameters = self.build_query_string(parameters)

        response: Response = self.get(f'{base_request_uri}{url_parameters}')

        consumption_data = json.loads(response.text)
        results_data = consumption_data['results']
        results = [Consumption(**result_entry) for result_entry in results_data]

        consumption: ClientResponse = ClientResponse(
            consumption_data['count'],
            consumption_data['next'],
            consumption_data['previous'],
            results)

        return consumption

    def get_products(self,
                     availability_date: datetime = None,
                     filtering: ProductFiltering = None
        ) -> list[Product]:
        """
        Retrieves product data from the Octopus Energy API.

        Returns:
            list[Product]: A list of product data.
        """
        product_data: list[Product] = []
        is_next: bool = True
        page: int = 1
        while is_next:
            products: ClientResponse = self.get_proucts_page(availability_date,
                                                             filtering,
                                                             page)
            product_data += products.results
            page += 1
            if products.next is None:
                is_next = False

        return product_data

    def get_proucts_page(self,
                         availability_date: datetime = None,
                         filtering: ProductFiltering = None,
                         page: int = 1
        ) -> ClientResponse:
        """
        Retrieves a specific page of product data from the Octopus Energy API.

        Args:
            is_variable (bool, optional): A value indicating whether the product is variable.
                Defaults to None.
            is_green (bool, optional): A value indicating whether the product is green.
                Defaults to None.
            is_tracker (bool, optional): A value indicating whether the product is a tracker.
                Defaults to None.
            is_prepay (bool, optional): A value indicating whether the product is prepay.
                Defaults to None.
            is_business (bool, optional): A value indicating whether the product is for business.
                Defaults to None.
            available_at (datetime, optional): The date and time the product is available.
                Defaults to None.
        
        Returns:
            ClientResponse[Product]: The specified page of product data.
        """
        base_request_uri: str = f'{BASE_URI}/products'
        parameters: dict[str, str] = {}
        if filtering and ProductFiltering.VARIABLE in filtering:
            parameters['is_variable'] = TRUE
        if filtering and ProductFiltering.GREEN in filtering:
            parameters['is_green'] = TRUE
        if filtering and ProductFiltering.TRACKER in filtering:
            parameters['is_tracker'] = TRUE
        if filtering and ProductFiltering.PREPAY in filtering:
            parameters['is_prepay'] = TRUE
        if filtering and ProductFiltering.BUSINESS in filtering:
            parameters['is_business'] = TRUE
        if availability_date:
            parameters['available_at'] = availability_date.isoformat()
        if page:
            parameters['page'] = page

        url_parameters: str = ''
        if len(parameters) > 0:
            url_parameters = self.build_query_string(parameters)

        response: Response = self.get(f'{base_request_uri}{url_parameters}')

        product_data = json.loads(response.text)
        results_data = product_data['results']
        results = [Product(**result_entry) for result_entry in results_data]

        products: ClientResponse = ClientResponse(
            product_data['count'],
            product_data['next'],
            product_data['previous'],
            results)

        return products

    def build_query_string(self, parameters: dict[str, str]) -> str:
        """
        Builds a query string from the specified parameters.

        Args:
            parameters (dict[str, str]): The parameters to build the query string from.

        Returns:
            str: The query string.
        """
        return f'?{'&'.join([f'{key}={value}' for key, value in parameters.items()])}'

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

class OctopusEnergyClientFactory:
    """
    Factory for creating Octopus Energy clients.
    """

    def create(self,
               client_type: Literal['API'] = 'API',
               api_key: str = None,
               account_number: str = None,
               meter_mpan: str = None,
               meter_serial: str = None
        ) -> OctopusEnergyClientBase:
        """
        Creates an Octopus Energy client.

        Args:
            client_type (Literal['API'], optional): The type of client to create.
                Defaults to API.
            api_key (str): The API key for accessing the Octopus Energy API.
                Defaults to None.
            account_number (str, optional): The Octopus Energy account number.
                Defaults to None.
            meter_mpan (str, optional): The Meter Point Administration Number (MPAN) for the meter.
                Defaults to None.
            meter_serial (str, optional): The serial number for the meter.
                Defaults to None.

        Returns:
            OctopusEnergyClientBase: The Octopus Energy client.
        """
        match client_type:
            case 'API':
                if not all([api_key, account_number, meter_mpan, meter_serial]):
                    raise ValueError('The API client requires an API key, account number, meter MPAN and serial number.')

                return OctopusEnergyClient(api_key,
                                           account_number,
                                           meter_mpan,
                                           meter_serial)
            case _:
                pass
