"""
CLI commands for the agent MCP server.
"""

import click
from mcp.server.fastmcp import FastMCP
from . import create_json_output, OCTOPUS_ENERGY_REPOSITORY

mcp_server: FastMCP = FastMCP()

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
    mcp_server.run()

@mcp_server.tool('get_account', 'Get Octopus Energy account details.')
def get_account() -> str:
    """
    Gets the Octopus Energy account details.

    Returns:
        str: The account details as a JSON object.
    """
    return create_json_output(OCTOPUS_ENERGY_REPOSITORY.get_account())
