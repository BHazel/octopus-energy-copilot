"""
CLI commands for the agent MCP server.
"""

from datetime import datetime
import click
from mcp.server.fastmcp import FastMCP
from octopus_energy.model import ConsumptionGrouping
from . import create_json_output, OCTOPUS_ENERGY_REPOSITORY

MCP_SERVER: FastMCP = FastMCP()

@click.group('mcp')
def mcp_server_group():
    """
    Commands for the agent MCP server.
    """

@mcp_server_group.command('run')
def run_mcp_server():
    """
    Run the MCP server.
    """
    print("Octopus Energy Copilot MCP server is running...")
    MCP_SERVER.run()

@MCP_SERVER.tool('oec_get_account', 'Get Octopus Energy account details.')
def get_account() -> str:
    """
    Gets the Octopus Energy account details.

    Returns:
        str: The account details as a JSON object.
    """
    return create_json_output(OCTOPUS_ENERGY_REPOSITORY.get_account())

@MCP_SERVER.tool('oec_get_max_consumption',
                 'Get the period with the maximum consumption within a specified date-time range.')
def get_max_consumption(from_date: str = None,
                        to_date: str = None,
                        period: ConsumptionGrouping = 'half-hour'
    ) -> str:
    """
    Gets the data for the period of maximum consumption as a JSON object,
    containing the consumption in kWh and the start and end dates, from the Octopus
    Energy API.  By default the period is 30 minutes, provided as 'half-hour', but
    other possibilities include an hour ('hour'), a day ('day'), a week ('week'),
    a month ('month') and a quarter ('quarter').

    Args:
        from_date: The start date for the period in ISO-8601 format excluding time zone information.
        to_date: The end date for the period in ISO-8601 format excluding time zone information.
        period: The period of time to group the consumption data by.
            Possible Values: 'half-hour', 'hour', 'day', 'week', 'month', 'quarter'.

    Returns:
        str: The consumption data for the period of maximum consumption
        as a JSON object, including the consumption value in kWh and the start and
        end date and times of the period.
    """
    start_date = datetime.fromisoformat(from_date) if from_date else None
    end_date = datetime.fromisoformat(to_date) if to_date else None

    max_consumption = OCTOPUS_ENERGY_REPOSITORY.get_max_consumption(start_date, end_date, period)
    return create_json_output(max_consumption)

@MCP_SERVER.tool('oec_get_min_consumption',
                 'Get the period with the minimum consumption within a specified date-time range.')
def get_min_consumption(from_date: str = None,
                        to_date: str = None,
                        period: ConsumptionGrouping = 'half-hour'
    ) -> str:
    """
    Gets the data for the period of minimum consumption as a JSON object,
    containing the consumption in kWh and the start and end dates, from the Octopus
    Energy API.  By default the period is 30 minutes, provided as 'half-hour', but
    other possibilities include an hour ('hour'), a day ('day'), a week ('week'),
    a month ('month') and a quarter ('quarter').

    Args:
        from_date: The start date for the period in ISO-8601 format excluding time zone information.
        to_date: The end date for the period in ISO-8601 format excluding time zone information.
        period: The period of time to group the consumption data by.
            Possible Values: 'half-hour', 'hour', 'day', 'week', 'month', 'quarter'.

    Returns:
        str: The consumption data for the period of minimum consumption
        as a JSON object, including the consumption value in kWh and the start and
        end date and times of the period.
    """
    start_date = datetime.fromisoformat(from_date) if from_date else None
    end_date = datetime.fromisoformat(to_date) if to_date else None

    min_consumption = OCTOPUS_ENERGY_REPOSITORY.get_min_consumption(start_date, end_date, period)
    return create_json_output(min_consumption)

@MCP_SERVER.tool('oec_get_total_consumption',
                 'Get the total consumption within a specified date-time range.')
def get_total_consumption(from_date: str = None,
                          to_date: str = None
    ) -> str:
    """
    Gets the total consumption for a given period from the Octopus Energy API as a JSON object,
    containing the consumption in kWh and the start and end dates, from the Octopus Energy API.

    Args:
        from_date: The start date for the period in ISO-8601 format excluding time zone information.
        to_date: The end date for the period in ISO-8601 format excluding time zone information.

    Returns:
        str: The total consumption data for the given period as a JSON object
            including the consumption value in kWh and the start and end date
            and times of the period.
    """
    start_date = datetime.fromisoformat(from_date) if from_date else None
    end_date = datetime.fromisoformat(to_date) if to_date else None

    total_consumption = OCTOPUS_ENERGY_REPOSITORY.get_total_consumption(start_date, end_date)
    return create_json_output(total_consumption)
