"""
Main program entry point.
"""

from datetime import datetime
from octopus_energy.client import OctopusEnergyClient
from octopus_energy.model import Consumption

OCTOPUS_ENERGY_API_KEY: str = ''
METER_MPAN: str = ''
METER_SERIAL: str = ''
client: OctopusEnergyClient = OctopusEnergyClient(
    OCTOPUS_ENERGY_API_KEY,
    METER_MPAN,
    METER_SERIAL)

consumption: list[Consumption] = client.get_consumption(
    from_date=datetime(2024, 4, 1, 0, 0),
    to_date=datetime(2024, 4, 3, 4, 0))

for result in consumption:
    print(f'{result.consumption} kWh for {result.interval_start} to {result.interval_end}')
