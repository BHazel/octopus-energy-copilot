"""
CLI commands for electricity consumption.
"""

from datetime import datetime, timedelta
import os
import click
from dotenv import load_dotenv
from gradio import Dropdown, Interface, Textbox
from cli import create_json_output
from energy.conversion import convert_to_co2, kWh
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
                    grouping: str = 'half-hour',
                    query: str = None,
                    co2: bool = False
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
                    grouping: str = 'half-hour',
                    query: str = None,
                    co2: bool = False
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
                    grouping: str = 'half-hour',
                    query: str = None,
                    co2: bool = False
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
    repository: OctopusEnergyRepository = OctopusEnergyRepository(
        OctopusEnergyClient(
            api_key,
            None,
            meter_mpan,
            meter_serial))

    total_consumption: Consumption = repository.get_total_consumption(
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
    repository: OctopusEnergyRepository = OctopusEnergyRepository(
        OctopusEnergyClient(
            api_key,
            None,
            meter_mpan,
            meter_serial))

    def load_consumption_ui(api_key: str,
                            meter_mpan: str,
                            meter_serial: str,
                            data_to_retrieve: str,
                            from_date: str,
                            to_date: str,
                            group: str,
                            query: str):
        """
        Loads the consumption UI.

        Args:
            api_key (str): The API key.
            meter_mpan (str): The meter MPAN.
            meter_serial (str): The meter serial number.
            data_to_retrieve (str): The consumption data to retrieve.
            from_date (str): The start date.
            to_date (str): The end date.
            group (str): The consumption grouping.
            query (str): The JMESPath query.
        """
        consumption_function = map_ui_data_to_retrieve_to_function(data_to_retrieve, repository)
        interval_start = datetime.fromisoformat(from_date) if from_date else None
        interval_end = datetime.fromisoformat(to_date) if to_date else None
        grouping = map_ui_grouping_to_consumption_grouping(group)
        consumption_data = consumption_function(from_date=interval_start,
                                                to_date=interval_end,
                                                grouping=grouping)

        output = create_json_output(consumption_data, query)
        return output

    default_from_date = (datetime.now() - timedelta(days=1)).replace(minute=0,
                                                                     second=0,
                                                                     microsecond=0)
    default_to_date = datetime.now().replace(minute=0, second=0, microsecond=0)
    interface = Interface(load_consumption_ui,
                          inputs=[
                              Textbox(label='API Key', type='password', value=api_key),
                              Textbox(label='Meter MPAN', value=meter_mpan),
                              Textbox(label='Meter Serial', value=meter_serial),
                              Dropdown(label='Data to Retrieve', value='List', choices=[
                                  'List',
                                  'Maximum',
                                  'Minimum',
                                  'Total'
                              ]),
                              Textbox(label='From Date', value=default_from_date.isoformat()),
                              Textbox(label='To Date', value=default_to_date.isoformat()),
                              Dropdown(label='Grouping', value='Half Hour', choices=[
                                    'Half Hour',
                                    'Hour',
                                    'Day',
                                    'Week',
                                    'Month',
                                    'Quarter'
                                ]),
                              Textbox(label='JMESPath Query')
                          ],
                          outputs='json')
    interface.launch(inbrowser=open_in_browser)

def get_consumption_grouping(grouping: str) -> ConsumptionGrouping:
    """
    Gets the consumption grouping from the CLI input.

    Args:
        grouping (str): The grouping from CLI input.
    
    Returns:
        ConsumptionGrouping: The consumption grouping.
    """
    converted_grouping: str = None if grouping == 'half-hour' else grouping
    return ConsumptionGrouping(converted_grouping)

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

def map_ui_data_to_retrieve_to_function(data_to_retrieve: str, repository: OctopusEnergyRepository):
    """
    Maps the UI selection for the data to retrieve to the appropriate repository function.

    Args:
        data_to_retrieve (str): The data to retrieve.
        repository (OctopusEnergyRepository): The Octopus Energy repository.
    
    Returns:
        Callable: The function to retrieve the data.
    """
    match data_to_retrieve:
        case 'List':
            return repository.get_consumption
        case 'Maximum':
            return repository.get_max_consumption
        case 'Minimum':
            return repository.get_min_consumption
        case 'Total':
            return repository.get_total_consumption
        case _:
            return repository.get_consumption

def map_ui_grouping_to_consumption_grouping(grouping: str) -> ConsumptionGrouping:
    """
    Maps the UI selection for the grouping to the appropriate consumption grouping.

    Args:
        grouping (str): The grouping.
    
    Returns:
        ConsumptionGrouping: The consumption grouping.
    """
    match grouping:
        case 'Half Hour':
            consumption_grouping = ConsumptionGrouping.HALF_HOUR
        case 'Hour':
            consumption_grouping = ConsumptionGrouping.HOUR
        case 'Day':
            consumption_grouping = ConsumptionGrouping.DAY
        case 'Week':
            consumption_grouping = ConsumptionGrouping.WEEK
        case 'Month':
            consumption_grouping = ConsumptionGrouping.MONTH
        case 'Quarter':
            consumption_grouping = ConsumptionGrouping.QUARTER
        case _:
            consumption_grouping = ConsumptionGrouping.HALF_HOUR

    return consumption_grouping
