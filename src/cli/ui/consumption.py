"""
Builder for the web UI for the consumption CLI command.
"""

from datetime import datetime, timedelta
from gradio import Blocks, Dropdown, Interface, Textbox
from cli import create_json_output
from cli.ui import BaseUiBuilder
from octopus_energy.model import ConsumptionGrouping
from octopus_energy.repository import OctopusEnergyRepository

class ConsumptionUiBuilder(BaseUiBuilder):
    """
    Builds the web UI for the consumption CLI command.
    """
    DEFAULT_FROM_DATE = (datetime.now() - timedelta(days=1)).replace(minute=0,
                                                                     second=0,
                                                                     microsecond=0)
    DEFAULT_TO_DATE = datetime.now().replace(minute=0, second=0, microsecond=0)

    def __init__(self,
                 api_key: str,
                 meter_mpan: str,
                 meter_serial: str,
                 repository: OctopusEnergyRepository):
        """
        Initialises an instance of the ConsumptionUiBuilder class.

        Args:
            api_key (str): The API key.
            meter_mpan (str): The meter MPAN.
            meter_serial (str): The meter serial number.
            repository (OctopusEnergyRepository): The Octopus Energy repository.
        """
        self.api_key = api_key
        self.meter_mpan = meter_mpan
        self.meter_serial = meter_serial
        self.repository = repository

    def build_ui(self) -> Blocks:
        """
        Builds the web UI.
        """
        return Interface(self.load_consumption_ui,
                          inputs=[
                              Textbox(label='API Key', type='password', value=self.api_key),
                              Textbox(label='Meter MPAN', value=self.meter_mpan),
                              Textbox(label='Meter Serial', value=self.meter_serial),
                              Dropdown(label='Data to Retrieve', value='List', choices=[
                                  'List',
                                  'Maximum',
                                  'Minimum',
                                  'Total'
                              ]),
                              Textbox(label='From Date', value=self.DEFAULT_FROM_DATE.isoformat()),
                              Textbox(label='To Date', value=self.DEFAULT_TO_DATE.isoformat()),
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

    def load_consumption_ui(self,
                            api_key: str,
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
        consumption_function = map_ui_data_to_retrieve_to_function(data_to_retrieve,
                                                                   self.repository)
        interval_start = datetime.fromisoformat(from_date) if from_date else None
        interval_end = datetime.fromisoformat(to_date) if to_date else None
        grouping = map_ui_grouping_to_consumption_grouping(group)
        consumption_data = consumption_function(*[interval_start, interval_end, grouping])

        output = create_json_output(consumption_data, query)
        return output

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
