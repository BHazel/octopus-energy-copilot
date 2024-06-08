"""
AI tools for working with account data.
"""

import os
from dotenv import load_dotenv
import jsonpickle
from langchain_core.tools import tool
from octopus_energy.client import OctopusEnergyClient
from octopus_energy.repository import OctopusEnergyRepository

load_dotenv()

repository = OctopusEnergyRepository(
    OctopusEnergyClient(
        os.environ['OCTOPUS_ENERGY_API_KEY'],
        os.environ['OCTOPUS_ENERGY_ACCOUNT_NUMBER'],
        os.environ['OCTOPUS_ENERGY_METER_MPAN'],
        os.environ['OCTOPUS_ENERGY_METER_SERIAL']))

@tool
def get_account() -> str:
    """
    Gets the account details as a JSON object from the Octopus Energy API.

    Returns:
        str: The account details as a JSON object.
    """
    account = repository.get_account()
    return jsonpickle.encode(account)
