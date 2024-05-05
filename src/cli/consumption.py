"""
CLI commands for electricity consumption.
"""

from datetime import datetime
import os
import click
from dotenv import load_dotenv
from octopus_energy.client import OctopusEnergyClient
from octopus_energy.model import Consumption

load_dotenv()

@click.group('consumption')
def consumption_group():
    """
    Commands for electricity consumption.
    """

@consumption_group.command('list')
@click.option('--api-key', 'api_key',
              type=click.STRING,
              default=os.environ['OCTOPUS_ENERGY_API_KEY'],
              help='The Octopus Energy API key (Not recommended).')
@click.option('-m', '--meter-mpan', 'meter_mpan',
              type=click.STRING,
              default=os.environ['OCTOPUS_ENERGY_METER_MPAN'],
              help='The electricity meter MPAN.')
@click.option('-s', '--meter-serial', 'meter_serial',
              type=click.STRING,
              default=os.environ['OCTOPUS_ENERGY_METER_SERIAL'],
              help='The electricity meter serial number.')
@click.option('-f', '--from', 'from_date',
              type=click.DateTime(),
              help='From date.')
@click.option('-t', '--to', 'to_date',
              type=click.DateTime(),
              help='To date.')
def list_consumption(api_key: str,
                    meter_mpan: str,
                    meter_serial: str,
                    from_date: datetime = None,
                    to_date: datetime = None
    ):
    """
    Lists electricity consumption between two dates.
    """
    client: OctopusEnergyClient = OctopusEnergyClient(
        api_key,
        meter_mpan,
        meter_serial)

    consumption: list[Consumption] = client.get_consumption(
        from_date=from_date,
        to_date=to_date)

    for entry in consumption:
        print(f'{entry.consumption} kWh for {entry.interval_start} to {entry.interval_end}')

@consumption_group.command('max')
@click.option('--api-key', 'api_key',
              type=click.STRING,
              default=os.environ['OCTOPUS_ENERGY_API_KEY'],
              help='The Octopus Energy API key (Not recommended).')
@click.option('-m', '--meter-mpan', 'meter_mpan',
              type=click.STRING,
              default=os.environ['OCTOPUS_ENERGY_METER_MPAN'],
              help='The electricity meter MPAN.')
@click.option('-s', '--meter-serial', 'meter_serial',
              type=click.STRING,
              default=os.environ['OCTOPUS_ENERGY_METER_SERIAL'],
              help='The electricity meter serial number.')
@click.option('-f', '--from', 'from_date',
              type=click.DateTime(),
              help='From date.')
@click.option('-t', '--to', 'to_date',
              type=click.DateTime(),
              help='To date.')
def get_max_consumption(api_key: str,
                    meter_mpan: str,
                    meter_serial: str,
                    from_date: datetime = None,
                    to_date: datetime = None
    ):
    """
    Gets the maximum electricity consumption between two dates.
    """
    client: OctopusEnergyClient = OctopusEnergyClient(
        api_key,
        meter_mpan,
        meter_serial)

    consumption_list: list[Consumption] = client.get_consumption(
        from_date=from_date,
        to_date=to_date)

    max_consumption = max(consumption_list,
                          key=lambda entry: entry.consumption)
    
    print(f'{max_consumption.consumption} kWh between {max_consumption.interval_start} and {max_consumption.interval_end}')
