"""
Interconversion of energy values and related quantities.
"""

from pint import Quantity
from energy.units import kg, kWh

CO2_EMISSION_FACTOR_MAGNITUDE = 0.20707

def co2_emission_factor() -> Quantity:
    """
    Returns:
        Quantity: The CO2 emission factor for electricity in kg/kWh.
    """
    return CO2_EMISSION_FACTOR_MAGNITUDE * kg / kWh

def convert_to_co2(energy: Quantity) -> float:
    """
    Converts the given energy to the mass of CO2 saved in kg.

    Args:
        energy (Quantity): The energy to convert.

    Returns:
        Quantity: The energy converted to the mass of CO2 saved in kg.
    """
    energy_in_kwh = energy.to(kWh)
    mass_co2 = energy_in_kwh * co2_emission_factor()
    return mass_co2.magnitude
