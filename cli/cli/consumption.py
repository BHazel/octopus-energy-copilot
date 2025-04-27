"""
CLI commands for electricity consumption.
"""

from datetime import datetime
import os
import click
from energy.conversion import convert_to_co2
from energy.units import kWh
from octopus_energy.model import Consumption, ConsumptionGrouping
from . import create_json_output, OCTOPUS_ENERGY_REPOSITORY, update_client_credentials
from .ui.consumption import ConsumptionUiBuilder

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
@click.option('-q', '--query', 'query',
              type=click.STRING,
              default=None,
              help='The JMESPath query to filter and structure the output.')
@click.option('--co2', 'co2',
              type=click.BOOL,
              is_flag=True,
              help='Show consumption values in kg of CO2 saved.')
def list_consumption(api_key: str,
                    meter_mpan: str,
                    meter_serial: str,
                    from_date: datetime = None,
                    to_date: datetime = None,
                    grouping: ConsumptionGrouping = 'half-hour',
                    query: str = None,
                    co2: bool = False
    ):
    """
    Lists electricity consumption between two dates.
    """
    update_client_credentials(api_key=api_key,
                              meter_mpan=meter_mpan,
                              meter_serial=meter_serial)

    consumption: list[Consumption] = OCTOPUS_ENERGY_REPOSITORY.get_consumption(
        from_date=from_date,
        to_date=to_date,
        grouping=grouping)

    if co2:
        consumption = [convert_consumption_to_co2(c) for c in consumption]

    output = create_json_output(consumption, query)
    print(output)

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
@click.option('-q', '--query', 'query',
              type=click.STRING,
              default=None,
              help='The JMESPath query to filter and structure the output.')
@click.option('--co2', 'co2',
              type=click.BOOL,
              is_flag=True,
              help='Show consumption values in kg of CO2 saved.')
def get_max_consumption(api_key: str,
                    meter_mpan: str,
                    meter_serial: str,
                    from_date: datetime = None,
                    to_date: datetime = None,
                    grouping: ConsumptionGrouping = 'half-hour',
                    query: str = None,
                    co2: bool = False
    ):
    """
    Gets the maximum electricity consumption between two dates.
    """
    update_client_credentials(api_key=api_key,
                              meter_mpan=meter_mpan,
                              meter_serial=meter_serial)

    max_consumption: Consumption = OCTOPUS_ENERGY_REPOSITORY.get_max_consumption(
        from_date=from_date,
        to_date=to_date,
        grouping=grouping)

    if co2:
        max_consumption = convert_consumption_to_co2(max_consumption)

    output = create_json_output(max_consumption, query)
    print(output)

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
@click.option('-q', '--query', 'query',
              type=click.STRING,
              default=None,
              help='The JMESPath query to filter and structure the output.')
@click.option('--co2', 'co2',
              type=click.BOOL,
              is_flag=True,
              help='Show consumption values in kg of CO2 saved.')
def get_min_consumption(api_key: str,
                    meter_mpan: str,
                    meter_serial: str,
                    from_date: datetime = None,
                    to_date: datetime = None,
                    grouping: ConsumptionGrouping = 'half-hour',
                    query: str = None,
                    co2: bool = False
    ):
    """
    Gets the minimum electricity consumption between two dates.
    """
    update_client_credentials(api_key=api_key,
                              meter_mpan=meter_mpan,
                              meter_serial=meter_serial)

    min_consumption: Consumption = OCTOPUS_ENERGY_REPOSITORY.get_min_consumption(
        from_date=from_date,
        to_date=to_date,
        grouping=grouping)

    if co2:
        min_consumption = convert_consumption_to_co2(min_consumption)

    output = create_json_output(min_consumption, query)
    print(output)

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
@click.option('-q', '--query', 'query',
              type=click.STRING,
              default=None,
              help='The JMESPath query to filter and structure the output.')
@click.option('--co2', 'co2',
              type=click.BOOL,
              is_flag=True,
              help='Show consumption values in kg of CO2 saved.')
def get_total_consumption(api_key: str,
                    meter_mpan: str,
                    meter_serial: str,
                    from_date: datetime = None,
                    to_date: datetime = None,
                    query: str = None,
                    co2: bool = False
    ):
    """
    Gets the total electricity consumption between two dates.
    """
    update_client_credentials(api_key=api_key,
                              meter_mpan=meter_mpan,
                              meter_serial=meter_serial)

    total_consumption: Consumption = OCTOPUS_ENERGY_REPOSITORY.get_total_consumption(
        from_date=from_date,
        to_date=to_date)

    if co2:
        total_consumption = convert_consumption_to_co2(total_consumption)

    output = create_json_output(total_consumption, query)
    print(output)

@consumption_group.command('ui')
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
@click.option('-o', '--open', 'open_in_browser',
              type=click.BOOL,
              is_flag=True,
              help='Open the UI in the default web browser.')
def use_consumption_ui(api_key: str,
                        meter_mpan: str,
                        meter_serial: str,
                        open_in_browser: bool):
    """
    Use a web user interface to get electricity consumption data.
    """
    update_client_credentials(api_key=api_key,
                              meter_mpan=meter_mpan,
                              meter_serial=meter_serial)

    consumption_ui_builder = ConsumptionUiBuilder(api_key, meter_mpan, meter_serial, OCTOPUS_ENERGY_REPOSITORY)
    interface = consumption_ui_builder.build_ui()
    interface.launch(inbrowser=open_in_browser)

def convert_consumption_to_co2(consumption: Consumption) -> Consumption:
    """
    Converts consumption in kWh to kg of CO2.

    Args:
        consumption (Consumption): The consumption in kWh.
    
    Returns:
        Consumption: The consumption data in kg of CO2.
    """
    consumption_in_kwh = consumption.consumption * kWh
    consumption_in_co2 = round(convert_to_co2(consumption_in_kwh), 3)
    return Consumption(consumption_in_co2,
                       consumption.interval_start,
                       consumption.interval_end)
