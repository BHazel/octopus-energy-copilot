"""
Main program entry point.
"""

from datetime import datetime
import os
import click
from dotenv import load_dotenv
from octopus_energy.client import OctopusEnergyClient
from octopus_energy.model import Consumption

load_dotenv()

OCTOPUS_ENERGY_API_KEY: str = os.environ['OCTOPUS_ENERGY_API_KEY']
METER_MPAN: str = os.environ['OCTOPUS_ENERGY_METER_MPAN']
METER_SERIAL: str = os.environ['OCTOPUS_ENERGY_METER_SERIAL']

@click.group()
@click.version_option('0.0.1', prog_name='Octopus Energy Copilot CLI')
@click.help_option('-h', '--help')
def main():
    """
    Root command for the Octopus Energy Copilot CLI.
    """

@main.command('consumption')
@click.option('-f', '--from', 'from_date', type=click.DateTime(), help='From date.')
@click.option('-t', '--to', 'to_date', type=click.DateTime(), help='To date.')
def get_consumption(from_date: datetime = None, to_date: datetime = None):
    """
    Gets electricity consumption.
    """
    client: OctopusEnergyClient = OctopusEnergyClient(
        OCTOPUS_ENERGY_API_KEY,
        METER_MPAN,
        METER_SERIAL)

    consumption: list[Consumption] = client.get_consumption(
        from_date=from_date,
        to_date=to_date)

    for entry in consumption:
        print(f'{entry.consumption} kWh for {entry.interval_start} to {entry.interval_end}')

if __name__ == '__main__':
    main()
