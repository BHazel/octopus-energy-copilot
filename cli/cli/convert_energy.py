"""
CLI commands for working with energy and related values.
"""

import click
from pint import Quantity
from energy.conversion import (
    calculate_power_for_energy,
    convert_value,
    convert_to_co2
)
from energy.units import (
    ENERGY_UNITS,
    ENERGY_UNIT_MAP,
    DURATION_UNITS,
    DURATION_UNIT_MAP,
    POWER_UNITS,
    POWER_UNIT_MAP
)
from . import create_json_output

@click.group("energy")
def convert_energy_group():
    """
    Commands for working with energy and related values.
    """

@convert_energy_group.command("amount")
@click.option('--from', '-f', 'from_unit',
              type=click.Choice(ENERGY_UNITS),
              default='kWh',
              help='Unit to convert from.')
@click.option('--to', '-t', 'to_unit',
              type=click.Choice(ENERGY_UNITS),
              default='J',
              help='Unit to convert to.')
@click.argument('amount',
                type=float)
def interconvert_energy(from_unit: str,
                         to_unit: str,
                         amount: float
    ):
    """
    Convert an amount of energy from one unit to another.
    """
    sanitised_from_unit: Quantity = ENERGY_UNIT_MAP[from_unit.lower()]
    sanitised_to_unit: Quantity = ENERGY_UNIT_MAP[to_unit.lower()]

    input_amount: Quantity = amount * sanitised_from_unit
    converted_amount: float = convert_value(input_amount,
                                             sanitised_to_unit)

    print(create_json_output(converted_amount))

@convert_energy_group.command("co2")
@click.option('--unit', '-u', 'unit',
              type=click.Choice(ENERGY_UNITS),
              default='kWh',
              help='Unit of energy.')
@click.argument('amount',
                type=float)
def convert_to_co2_equivalent(unit: str,
                              amount: float
    ):
    """
    Convert an amount of energy to its equivalent mass of CO2.
    """
    sanitised_unit: Quantity = ENERGY_UNIT_MAP[unit.lower()]

    input_amount: Quantity = amount * sanitised_unit
    converted_amount: float = convert_to_co2(input_amount)

    print(create_json_output(converted_amount))

@convert_energy_group.command("power")
@click.option('--energy', '-e', 'energy_unit',
              type=click.Choice(ENERGY_UNITS),
              default='kWh',
              help='The unit of energy.')
@click.option('--duration', '-d', 'duration_unit',
              type=click.Choice(DURATION_UNITS),
              default='h',
              help='The unit of duration (time).')
@click.option('--to', '-t', 'power_unit',
              type=click.Choice(POWER_UNITS),
              default='W',
              help='The unit of power.')
@click.argument('energy_amount',
                type=float)
@click.argument('duration_amount',
                type=float)
def convert_to_power(energy_unit: str,
                     duration_unit: str,
                     power_unit: str,
                     energy_amount: float,
                     duration_amount: float
    ):
    """
    Calculate the power for a given amount of energy and duration.
    """
    sanitised_energy_unit: Quantity = ENERGY_UNIT_MAP[energy_unit.lower()]
    sanitised_duration_unit: Quantity = DURATION_UNIT_MAP[duration_unit.lower()]
    sanitised_power_unit: Quantity = POWER_UNIT_MAP[power_unit.lower()]

    input_energy: Quantity = energy_amount * sanitised_energy_unit
    input_duration: Quantity = duration_amount * sanitised_duration_unit

    power: float = calculate_power_for_energy(input_energy, input_duration, sanitised_power_unit)

    print(create_json_output(power))
