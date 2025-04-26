"""
CLI commands for the AI agent server.
"""

import click
from .agent_mcp import mcp_server_group

@click.group('agent')
def agent_group():
    """
    Commands for the AI agent server.
    """

agent_group.add_command(mcp_server_group)
