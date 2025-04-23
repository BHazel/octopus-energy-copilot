"""
CLI module.
"""

import os
from typing import Any
from dotenv import load_dotenv
import jmespath
import jsonpickle
from octopus_energy.client import OctopusEnergyClientFactory
from octopus_energy.repository import OctopusEnergyRepository

load_dotenv()

client_type = os.environ.get('OEC_OCTOPUS_ENERGY_CLIENT_TYPE')
CONVERTED_CLIENT_TYPE = client_type if client_type is not None and client_type != '' else 'API'

OCTOPUS_ENERGY_CLIENT = OctopusEnergyClientFactory().create(
    client_type=CONVERTED_CLIENT_TYPE,
    api_key=os.environ.get('OCTOPUS_ENERGY_API_KEY'),
    account_number=os.environ.get('OCTOPUS_ENERGY_ACCOUNT_NUMBER'),
    meter_mpan=os.environ.get('OCTOPUS_ENERGY_METER_MPAN'),
    meter_serial=os.environ.get('OCTOPUS_ENERGY_METER_SERIAL'))

OCTOPUS_ENERGY_REPOSITORY = OctopusEnergyRepository(client=OCTOPUS_ENERGY_CLIENT)

def create_json_output(value: Any, query: str = None) -> str:
    """
    Creates a JSON string from an object, optionally filtered and structured with a JMESPath query.

    Args:
        value (Any): The object to serialize.
        query (str, optional): The JMESPath query to filter and structure the output.
            Defaults to None.
    
    Returns:
        str: The filtered and structured JSON string.
    """
    if query:
        if isinstance(value, list):
            sanitised_value = [item.__dict__ for item in value]
        else:
            sanitised_value = value.__dict__

        value_to_encode = jmespath.search(query, sanitised_value)
    else:
        value_to_encode = value

    return jsonpickle.encode(value_to_encode, indent=True)

def update_client_credentials(api_key: str = None,
                              number: str = None,
                              meter_mpan: str = None,
                              meter_serial: str = None
    ) -> None:
    """
    Updates the credentials on the Octopus Energy client.

    Args:
        api_key: The Octopus Energy API key.
        number: The Octopus Energy account number.
        meter_mpan: The electricity meter MPAN.
        meter_serial: The electricity meter serial number.
    """
    if api_key is not None:
        OCTOPUS_ENERGY_REPOSITORY.client.api_key = api_key
    if number is not None:
        OCTOPUS_ENERGY_REPOSITORY.client.account_number = number
    if meter_mpan is not None:
        OCTOPUS_ENERGY_REPOSITORY.client.meter_mpan = meter_mpan
    if meter_serial is not None:
        OCTOPUS_ENERGY_REPOSITORY.client.meter_serial = meter_serial
