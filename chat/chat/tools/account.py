"""
AI tools for working with account data.
"""

from dotenv import load_dotenv
import jsonpickle
from langchain_core.tools import tool
from .. import OCTOPUS_ENERGY_REPOSITORY

load_dotenv()

@tool
def get_account() -> str:
    """
    Gets the account details as a JSON object from the Octopus Energy API.

    Returns:
        str: The account details as a JSON object.
    """
    account = OCTOPUS_ENERGY_REPOSITORY.get_account()
    return jsonpickle.encode(account)
