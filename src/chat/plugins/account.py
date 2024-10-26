"""
AI tools for working with account data.
"""

import os
from typing import Annotated
from dotenv import load_dotenv
import jsonpickle
from semantic_kernel.functions import kernel_function
from octopus_energy.client import OctopusEnergyClient
from octopus_energy.repository import OctopusEnergyRepository

load_dotenv()

class AccountPlugin:
    """
    AI plug-in for working with account data.
    """
    def __init__(self):
        self.repository = OctopusEnergyRepository(
            OctopusEnergyClient(
                os.environ['OCTOPUS_ENERGY_API_KEY'],
                os.environ['OCTOPUS_ENERGY_ACCOUNT_NUMBER'],
                os.environ['OCTOPUS_ENERGY_METER_MPAN'],
                os.environ['OCTOPUS_ENERGY_METER_SERIAL']))

    @kernel_function(name='get_account',
                    description="""
                        Gets the account details as a JSON object from the
                        Octopus Energy API.
                    """
    )
    def get_account(self) -> Annotated[str, 'The account details as a JSON object.']:
        """
        Gets the account details as a JSON object from the Octopus Energy API.

        Returns:
            str: The account details as a JSON object.
        """
        account = self.repository.get_account()
        return jsonpickle.encode(account)
