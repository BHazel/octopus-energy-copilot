"""
CLI commands for electricity consumption.
"""

from datetime import datetime
import os
import click
from dotenv import load_dotenv
import jsonpickle
from octopus_energy.client import OctopusEnergyClient
from octopus_energy.model import Consumption, ConsumptionGrouping
from octopus_energy.repository import OctopusEnergyRepository

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
@click.option('-g', '--group', 'grouping',
                type=click.Choice(['half-hour', 'hour', 'day', 'week', 'month', 'quarter']),
                default='half-hour',
                help='The grouping of the consumption data.')
def list_consumption(api_key: str,
                    meter_mpan: str,
                    meter_serial: str,
                    from_date: datetime = None,
                    to_date: datetime = None,
                    grouping: str = 'half-hour'
    ):
    """
    Lists electricity consumption between two dates.
    """
    repository: OctopusEnergyRepository = OctopusEnergyRepository(
        OctopusEnergyClient(
            api_key,
            None,
            meter_mpan,
            meter_serial))

    consumption: list[Consumption] = repository.get_consumption(
        from_date=from_date,
        to_date=to_date,
        grouping=get_consumption_grouping(grouping))

    print(jsonpickle.encode(consumption, indent=True))

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
@click.option('-g', '--group', 'grouping',
                type=click.Choice(['half-hour', 'hour', 'day', 'week', 'month', 'quarter']),
                default='half-hour',
                help='The grouping of the consumption data.')
def get_max_consumption(api_key: str,
                    meter_mpan: str,
                    meter_serial: str,
                    from_date: datetime = None,
                    to_date: datetime = None,
                    grouping: str = 'half-hour'
    ):
    """
    Gets the maximum electricity consumption between two dates.
    """
    repository: OctopusEnergyRepository = OctopusEnergyRepository(
        OctopusEnergyClient(
            api_key,
            None,
            meter_mpan,
            meter_serial))

    max_consumption: Consumption = repository.get_max_consumption(
        from_date=from_date,
        to_date=to_date,
        grouping=get_consumption_grouping(grouping))

    print(jsonpickle.encode(max_consumption, indent=True))

@consumption_group.command('min')
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
@click.option('-g', '--group', 'grouping',
                type=click.Choice(['half-hour', 'hour', 'day', 'week', 'month', 'quarter']),
                default='half-hour',
                help='The grouping of the consumption data.')
def get_min_consumption(api_key: str,
                    meter_mpan: str,
                    meter_serial: str,
                    from_date: datetime = None,
                    to_date: datetime = None,
                    grouping: str = 'half-hour'
    ):
    """
    Gets the minimum electricity consumption between two dates.
    """
    repository: OctopusEnergyRepository = OctopusEnergyRepository(
        OctopusEnergyClient(
            api_key,
            None,
            meter_mpan,
            meter_serial))

    min_consumption: Consumption = repository.get_min_consumption(
        from_date=from_date,
        to_date=to_date,
        grouping=get_consumption_grouping(grouping))

    print(jsonpickle.encode(min_consumption, indent=True))

@consumption_group.command('total')
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
def get_total_consumption(api_key: str,
                    meter_mpan: str,
                    meter_serial: str,
                    from_date: datetime = None,
                    to_date: datetime = None
    ):
    """
    Gets the total electricity consumption between two dates.
    """
    repository: OctopusEnergyRepository = OctopusEnergyRepository(
        OctopusEnergyClient(
            api_key,
            None,
            meter_mpan,
            meter_serial))

    total_consumption: Consumption = repository.get_total_consumption(
        from_date=from_date,
        to_date=to_date)

    print(jsonpickle.encode(total_consumption, indent=True))

def get_consumption_grouping(grouping: str) -> ConsumptionGrouping:
    """
    Gets the consumption grouping from the CLI input.
    """
    converted_grouping: str = None if grouping == 'half-hour' else grouping
    return ConsumptionGrouping(converted_grouping)
