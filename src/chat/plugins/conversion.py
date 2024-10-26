"""
AI tools for performing conversions of energy, power and related units.
"""

from typing import Annotated
from pint import Quantity
from semantic_kernel.functions import kernel_function
from energy.conversion import (
    calculate_energy_for_power,
    calculate_power_for_energy,
    convert_to_co2,
    convert_value
)
from energy.units import (
    DURATION_UNIT_MAP,
    ENERGY_UNIT_MAP,
    POWER_UNIT_MAP
)

class ConversionPlugin:
    """
    AI plug-in for performing conversions of energy, power and related units.
    """
    @kernel_function(name='convert_energy',
                     description="""
                        Converts an amount of energy from one unit to another.

                        Permitted units, with values in brackets are how they should be
                        provided to the tool, are:
                        * calorie ('cal')
                        * electronvolt ('ev')
                        * joule ('j')
                        * kilojoule ('kj')
                        * megajoule ('mj')
                        * watt-hour ('wh')
                        * kilowatt-hour ('kwh')
                        * megawatt-hour ('mwh')

                        If no from or to unit is provided then a default of kWh should be used.
                        If no amount is provided then a default of 1 should be used.
                        Please notify the user if a default unit or amount is used.
                    """)
    def convert_energy(self,
                       amount: float,
                       from_unit: str,
                       to_unit: str
        ) -> Annotated[float, 'The amount of energy in the new unit.']:
        """
        Converts an amount of energy from one unit to another.

        Permitted units, with values in brackets are how they should be
        provided to the tool, are:
        * calorie ('cal')
        * electronvolt ('ev')
        * joule ('j')
        * kilojoule ('kj')
        * megajoule ('mj')
        * watt-hour ('wh')
        * kilowatt-hour ('kwh')
        * megawatt-hour ('mwh')

        If no from or to unit is provided then a default of kWh should be used.
        If no amount is provided then a default of 1 should be used.
        Please notify the user if a default unit or amount is used.

        Args:
            amount (float): The amount of energy to convert.
            from_unit (str): The unit to convert from.
            to_unit (str): The unit to convert to.

        Returns:
            float: The amount of energy in the new unit.
        """
        return self.convert_amount(amount, from_unit, to_unit, ENERGY_UNIT_MAP)

    @kernel_function(name='calculate_energy',
                     description="""
                        Calculates the energy for an amount of power over a given time period.

                        Permitted power units, with values in brackets are how they should be
                        provided to the tool, are:
                        * watt ('w')
                        * kilowatt ('kw')
                        * megawatt ('mw')

                        Permitted energy units, with values in brackets are how they should be
                        provided to the tool, are:
                        * calorie ('cal')
                        * electronvolt ('ev')
                        * joule ('j')
                        * kilojoule ('kj')
                        * megajoule ('mj')
                        * watt-hour ('wh')
                        * kilowatt-hour ('kwh')
                        * megawatt-hour ('mwh')

                        Permitted time units, with values in brackets are how they should be
                        provided to the tool, are:
                        * second ('s')
                        * minute ('min')
                        * hour ('h')

                        If a unit is not provided for a quantity then a default should be used:
                        * Power unit: W
                        * Energy unit: kWh
                        * Time unit: h
                        If no amount is provided then a default of 1 should be used.
                        Please notify the user if a default unit or amount is used.
                    """)
    def calculate_energy(self,
                         power_amount: float,
                         time_amount: float,
                         power_unit: str,
                         time_unit: str,
                         energy_unit: str
        ) -> Annotated[float, """
                        The amount of energy for the amount of power over the given time period.
                       """]:
        """
        Calculates the energy for an amount of power over a given time period.

        Permitted power units, with values in brackets are how they should be
        provided to the tool, are:
        * watt ('w')
        * kilowatt ('kw')
        * megawatt ('mw')

        Permitted energy units, with values in brackets are how they should be
        provided to the tool, are:
        * calorie ('cal')
        * electronvolt ('ev')
        * joule ('j')
        * kilojoule ('kj')
        * megajoule ('mj')
        * watt-hour ('wh')
        * kilowatt-hour ('kwh')
        * megawatt-hour ('mwh')

        Permitted time units, with values in brackets are how they should be
        provided to the tool, are:
        * second ('s')
        * minute ('min')
        * hour ('h')

        If a unit is not provided for a quantity then a default should be used:
        * Power unit: W
        * Energy unit: kWh
        * Time unit: h
        If no amount is provided then a default of 1 should be used.
        Please notify the user if a default unit or amount is used.

        Args:
            power_amount (float): The amount of power to calculate energy for.
            time_amount (float): The time period to calculate energy over.
            power_unit (str): The unit of power.
            time_unit (str): The unit of time.
            energy_unit (str): The unit of energy.

        Returns:
            float: The amount of energy for the amount of power over the given time period.
        """
        sanitised_power_unit = POWER_UNIT_MAP[power_unit.lower()]
        sanitised_time_unit = DURATION_UNIT_MAP[time_unit.lower()]
        sanitised_energy_unit = ENERGY_UNIT_MAP[energy_unit.lower()]

        input_power = power_amount * sanitised_power_unit
        input_duration = time_amount * sanitised_time_unit

        return calculate_energy_for_power(input_power, input_duration, sanitised_energy_unit)

    @kernel_function(name='convert_power',
                     description="""
                        Converts an amount of power from one unit to another.

                        Permitted units, with values in brackets are how they should be
                        provided to the tool, are:
                        * watt ('w')
                        * kilowatt ('kw')
                        * megawatt ('mw')

                        If no from or to unit is provided then a default of W should be used.
                        If no amount is provided then a default of 1 should be used.
                        Please notify the user if a default unit or amount is used.
                    """)
    def convert_power(self,
                      amount: float,
                      from_unit: str,
                      to_unit: str
        ) -> Annotated[float, """
                        The amount of power in the new unit.
                       """]:
        """
        Converts an amount of power from one unit to another.

        Permitted units, with values in brackets are how they should be
        provided to the tool, are:
        * watt ('w')
        * kilowatt ('kw')
        * megawatt ('mw')

        If no from or to unit is provided then a default of W should be used.
        If no amount is provided then a default of 1 should be used.
        Please notify the user if a default unit or amount is used.

        Args:
            amount (float): The amount of power to convert.
            from_unit (str): The unit to convert from.
            to_unit (str): The unit to convert to.

        Returns:
            float: The amount of power in the new unit.
        """
        return self.convert_amount(amount, from_unit, to_unit, POWER_UNIT_MAP)

    @kernel_function(name='calculate_power',
                     description="""
                        Calculates the power for an amount of energy over a given time period.

                        Permitted energy units, with values in brackets are how they should be
                        provided to the tool, are:
                        * calorie ('cal')
                        * electronvolt ('ev')
                        * joule ('j')
                        * kilojoule ('kj')
                        * megajoule ('mj')
                        * watt-hour ('wh')
                        * kilowatt-hour ('kwh')
                        * megawatt-hour ('mwh')

                        Permitted power units, with values in brackets are how they should be
                        provided to the tool, are:
                        * watt ('w')
                        * kilowatt ('kw')
                        * megawatt ('mw')

                        Permitted time units, with values in brackets are how they should be
                        provided to the tool, are:
                        * second ('s')
                        * minute ('min')
                        * hour ('h')

                        If a unit is not provided for a quantity then a default should be used:
                        * Energy unit: kWh
                        * Power unit: W
                        * Time unit: h
                        If no amount is provided then a default of 1 should be used.
                        Please notify the user if a default unit or amount is used.
                    """)
    def calculate_power(self,
                        energy_amount: float,
                        time_amount: float,
                        energy_unit: str,
                        time_unit: str,
                        power_unit: str
        ) -> Annotated[float, """
                        The power for the amount of energy over the given time period.
                       """]:
        """
        Calculates the power for an amount of energy over a given time period.

        Permitted energy units, with values in brackets are how they should be
        provided to the tool, are:
        * calorie ('cal')
        * electronvolt ('ev')
        * joule ('j')
        * kilojoule ('kj')
        * megajoule ('mj')
        * watt-hour ('wh')
        * kilowatt-hour ('kwh')
        * megawatt-hour ('mwh')

        Permitted power units, with values in brackets are how they should be
        provided to the tool, are:
        * watt ('w')
        * kilowatt ('kw')
        * megawatt ('mw')

        Permitted time units, with values in brackets are how they should be
        provided to the tool, are:
        * second ('s')
        * minute ('min')
        * hour ('h')

        If a unit is not provided for a quantity then a default should be used:
        * Energy unit: kWh
        * Power unit: W
        * Time unit: h
        If no amount is provided then a default of 1 should be used.
        Please notify the user if a default unit or amount is used.

        Args:
            energy_amount (float): The amount of energy to calculate power for.
            time_amount (float): The time period to calculate power over.
            energy_unit (str): The unit of energy.
            time_unit (str): The unit of time.
            power_unit (str): The unit of power.
        
        Returns:
            float: The power for the amount of energy over the given time period.
        """
        sanitised_energy_unit = ENERGY_UNIT_MAP[energy_unit.lower()]
        sanitised_time_unit = DURATION_UNIT_MAP[time_unit.lower()]
        sanitised_power_unit = POWER_UNIT_MAP[power_unit.lower()]

        input_energy = energy_amount * sanitised_energy_unit
        input_duration = time_amount * sanitised_time_unit

        return calculate_power_for_energy(input_energy, input_duration, sanitised_power_unit)

    @kernel_function(name='convert_energy_to_co2',
                     description="""
                        Converts an amount of energy to the mass of CO2 saved in kg.

                        Permitted units, with values in brackets are how they should be
                        provided to the tool, are:
                        * calorie ('cal')
                        * electronvolt ('ev')
                        * joule ('j')
                        * kilojoule ('kj')
                        * megajoule ('mj')
                        * watt-hour ('wh')
                        * kilowatt-hour ('kwh')
                        * megawatt-hour ('mwh')

                        If no unit is provided then a default of kWh should be used.
                        If no amount is provided then a default of 1 should be used.
                        Please notify the user if a default unit or amount is used.
                    """)
    def convert_energy_to_co2(self,
                              energy: float,
                              unit: str
        ) -> Annotated[float, """
                        The consumption value converted to the mass of CO2 saved in kg.
                       """]:
        """
        Converts an amount of energy to the mass of CO2 saved in kg.

        Permitted units, with values in brackets are how they should be
        provided to the tool, are:
        * calorie ('cal')
        * electronvolt ('ev')
        * joule ('j')
        * kilojoule ('kj')
        * megajoule ('mj')
        * watt-hour ('wh')
        * kilowatt-hour ('kwh')
        * megawatt-hour ('mwh')

        If no unit is provided then a default of kWh should be used.
        If no amount is provided then a default of 1 should be used.
        Please notify the user if a default unit or amount is used.

        Args:
            consumption: The consumption value in kWh.

        Returns:
            float: The consumption value converted to the mass of CO2 saved in kg.
        """
        sanitised_unit = ENERGY_UNIT_MAP[unit.lower()]
        converted_energy = energy * sanitised_unit
        return convert_to_co2(converted_energy)

    def convert_amount(self,
                       amount: float,
                       from_unit: str,
                       to_unit: str,
                       unit_map: dict[str, Quantity]
        ) -> float:
        """
        Converts an amount from one unit into another.

        Args:
            amount (float): The amount to convert.
            from_unit (str): The unit to convert from.
            to_unit (str): The unit to convert to.
            unit_map (dict[str, Quantity]): The mapping of unit symbols to their
                corresponding quantities.
        """
        sanitised_from_unit = unit_map[from_unit.lower()]
        sanitised_to_unit = unit_map[to_unit.lower()]

        input_amount = amount * sanitised_from_unit
        converted_amount = convert_value(input_amount, sanitised_to_unit)
        return converted_amount
