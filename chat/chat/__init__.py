"""
Chat module.
"""

import os
from dotenv import load_dotenv
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
