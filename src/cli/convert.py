"""
CLI commands for conversions.
"""

import click
from cli.convert_energy import convert_energy_group
from cli.convert_power import convert_power_group

@click.group("convert")
def convert_group():
    """
    Commands for performing conversions between different units.
    """

convert_group.add_command(convert_energy_group)
convert_group.add_command(convert_power_group)
