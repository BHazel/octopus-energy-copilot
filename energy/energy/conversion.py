"""
Interconversion of energy values and related quantities.
"""

from pint import Quantity
from .units import kg, kWh

CO2_EMISSION_FACTOR_MAGNITUDE = 0.20707

def co2_emission_factor() -> Quantity:
    """
    Returns:
        Quantity: The CO2 emission factor for electricity in kg/kWh.
    """
    return CO2_EMISSION_FACTOR_MAGNITUDE * kg / kWh

def convert_value(amount: Quantity,
                  to_unit: Quantity
    ) -> float:
    """
    Convert an amount from one unit to another.
    """
    converted_value = amount.to(to_unit)
    return converted_value.magnitude

def calculate_power_for_energy(energy: Quantity,
                               duration: Quantity,
                               to_unit: Quantity
    ) -> float:
    """
    Convert an amount of energy to power with a given duration.
    """
    if not energy.check('[energy]'):
        raise ValueError('Energy must have units of energy.')

    if not duration.check('[time]'):
        raise ValueError('Duration must have units of time.')

    if duration.magnitude == 0:
        raise ValueError('Duration must have a value greater than 0.')

    if not to_unit.check('[power]'):
        raise ValueError('Unit to convert to must have units of power.')

    power = energy / duration
    converted_power = power.to(to_unit)
    return converted_power.magnitude

def calculate_energy_for_power(power: Quantity,
                               duration: Quantity,
                               to_unit: Quantity
    ) -> float:
    """
    Convert an amount of power to energy with a given duration.
    """
    if not power.check('[power]'):
        raise ValueError('Power must have units of power.')

    if not duration.check('[time]'):
        raise ValueError('Duration must have units of time.')

    if not to_unit.check('[energy]'):
        raise ValueError('Unit to convert to must have units of energy.')

    energy = power * duration
    converted_energy = energy.to(to_unit)
    return converted_energy.magnitude

def convert_to_co2(energy: Quantity) -> float:
    """
    Converts the given energy to the mass of CO2 saved in kg.

    Args:
        energy (Quantity): The energy to convert.

    Returns:
        Quantity: The energy converted to the mass of CO2 saved in kg.
    """
    if not energy.check('[energy]'):
        raise ValueError('Energy must have units of energy.')

    energy_in_kwh = energy.to(kWh)
    mass_co2 = energy_in_kwh * co2_emission_factor()
    return mass_co2.magnitude
