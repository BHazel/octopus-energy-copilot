"""
CLI commands for working with power and related values.
"""

import click
from pint import Quantity
from cli import create_json_output
from energy.conversion import calculate_energy_for_power, convert_value
from energy.units import (
    ENERGY_UNITS,
    ENERGY_UNIT_MAP,
    DURATION_UNITS,
    DURATION_UNIT_MAP,
    POWER_UNITS,
    POWER_UNIT_MAP
)

@click.group("power")
def convert_power_group():
    """
    Commands for working with power and related values.
    """

@convert_power_group.command("amount")
@click.option('--from', '-f', 'from_unit',
              type=click.Choice(POWER_UNITS),
              default='W',
              help='Unit to convert from.')
@click.option('--to', '-t', 'to_unit',
              type=click.Choice(POWER_UNITS),
              default='hp',
              help='Unit to convert to.')
@click.argument('amount',
                type=float)
def interconvert_energy(from_unit: str,
                         to_unit: str,
                         amount: float
    ):
    """
    Convert an amount of power from one unit to another.
    """
    sanitised_from_unit: Quantity = POWER_UNIT_MAP[from_unit.lower()]
    sanitised_to_unit: Quantity = POWER_UNIT_MAP[to_unit.lower()]

    input_amount: Quantity = amount * sanitised_from_unit
    converted_amount: float = convert_value(input_amount,
                                             sanitised_to_unit)

    print(create_json_output(converted_amount))

@convert_power_group.command("energy")
@click.option('--power', '-p', 'power_unit',
              type=click.Choice(POWER_UNITS),
              default='W',
              help='The unit of power.')
@click.option('--duration', '-d', 'duration_unit',
              type=click.Choice(DURATION_UNITS),
              default='h',
              help='The unit of duration (time).')
@click.option('--to', '-t', 'energy_unit',
              type=click.Choice(ENERGY_UNITS),
              default='kWh',
              help='The unit of energy.')
@click.argument('power_amount',
                type=float)
@click.argument('duration_amount',
                type=float)
def convert_to_power(power_unit: str,
                     duration_unit: str,
                     energy_unit: str,
                     power_amount: float,
                     duration_amount: float
    ):
    """
    Calculate the energy for a given amount of power and duration.
    """
    sanitised_power_unit: Quantity = POWER_UNIT_MAP[power_unit.lower()]
    sanitised_duration_unit: Quantity = DURATION_UNIT_MAP[duration_unit.lower()]
    sanitised_energy_unit: Quantity = ENERGY_UNIT_MAP[energy_unit.lower()]

    input_power: Quantity = power_amount * sanitised_power_unit
    input_duration: Quantity = duration_amount * sanitised_duration_unit

    power: float = calculate_energy_for_power(input_power, input_duration, sanitised_energy_unit)

    print(create_json_output(power))
