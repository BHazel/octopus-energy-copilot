"""
Tests for the conversion module.
"""
import unittest
from pint import Quantity, set_application_registry
from pint.errors import DimensionalityError
from energy import UNIT_REGISTRY
from energy.conversion import (
    calculate_energy_for_power,
    calculate_power_for_energy,
    co2_emission_factor,
    convert_to_co2,
    convert_value
)

class ConversionTests(unittest.TestCase):
    """
    Tests for the conversion module.
    """
    def test_co2_emission_factor_returns_quantity(self):
        """
        Tests that the co2_emission_factor function returns the CO2 emission factor as a Quantity.
        """
        actual_co2_emission_factor: Quantity = co2_emission_factor()

        expected_co2_emission_factor: Quantity = Quantity(0.20707, 'kg/kWh')
        self.assertEqual(expected_co2_emission_factor, actual_co2_emission_factor)

    def test_convert_value_with_compatible_units_returns_converted_value(self):
        """
        Tests that the convert_value function returns the converted value when given compatible units.
        """
        amount: Quantity = Quantity(1000, 'kJ')
        to_unit: Quantity = Quantity(1, 'kWh')

        converted_value: float = convert_value(amount, to_unit)

        expected_value: float = 0.2778
        self.assertAlmostEqual(expected_value, converted_value, places=4)

    def test_convert_value_with_incompatible_units_raises_error(self):
        """
        Tests that the convert_value function raises an error when given incompatible units.
        """
        amount: Quantity = Quantity(1000, 'kJ')
        to_unit: Quantity = Quantity(1, 'kg')

        with self.assertRaises(DimensionalityError):
            convert_value(amount, to_unit)

    def test_calculate_power_for_energy_with_valid_units_returns_converted_value(self):
        """
        Tests that the calculate_power_for_energy function returns the converted power when given valid units.
        """
        energy: Quantity = Quantity(1000, 'kJ')
        duration: Quantity = Quantity(1, 'h')
        to_unit: Quantity = Quantity(1, 'kW')

        converted_power: float = calculate_power_for_energy(energy, duration, to_unit)

        expected_power: float = 0.2778
        self.assertAlmostEqual(expected_power, converted_power, places=4)

    def test_calculate_power_for_energy_with_invalid_energy_unit_raises_error(self):
        """
        Tests that the calculate_power_for_energy function raises an error when given an invalid energy unit.
        """
        energy: Quantity = Quantity(1000, 'kg')
        duration: Quantity = Quantity(1, 'h')
        to_unit: Quantity = Quantity(1, 'kW')

        with self.assertRaises(ValueError):
            calculate_power_for_energy(energy, duration, to_unit)

    def test_calculate_power_for_energy_with_invalid_duration_unit_raises_error(self):
        """
        Tests that the calculate_power_for_energy function raises an error when given an invalid duration unit.
        """
        energy: Quantity = Quantity(1000, 'kJ')
        duration: Quantity = Quantity(1, 'kg')
        to_unit: Quantity = Quantity(1, 'kW')

        with self.assertRaises(ValueError):
            calculate_power_for_energy(energy, duration, to_unit)

    def test_calculate_power_for_energy_with_invalid_duration_value_raises_error(self):
        """
        Tests that the calculate_power_for_energy function raises an error when given an invalid duration value.
        """
        energy: Quantity = Quantity(1000, 'kJ')
        duration: Quantity = Quantity(0, 'h')
        to_unit: Quantity = Quantity(1, 'kW')

        with self.assertRaises(ValueError):
            calculate_power_for_energy(energy, duration, to_unit)

    def test_calculate_power_for_energy_with_invalid_power_unit_raises_error(self):
        """
        Tests that the calculate_power_for_energy function raises an error when given an invalid power unit.
        """
        energy: Quantity = Quantity(1000, 'kJ')
        duration: Quantity = Quantity(1, 'h')
        to_unit: Quantity = Quantity(1, 'kg')

        with self.assertRaises(ValueError):
            calculate_power_for_energy(energy, duration, to_unit)

    def test_calculate_energy_for_power_with_valid_units_returns_converted_value(self):
        """
        Tests that the calculate_energy_for_power function returns the converted energy when given valid units.
        """
        power: Quantity = Quantity(0.2778, 'kW')
        duration: Quantity = Quantity(1, 'h')
        to_unit: Quantity = Quantity(1, 'kJ')

        converted_energy: float = calculate_energy_for_power(power, duration, to_unit)

        expected_energy: float = 1000.08
        self.assertAlmostEqual(expected_energy, converted_energy, places=4)

    def test_calculate_energy_for_power_with_invalid_power_unit_raises_error(self):
        """
        Tests that the calculate_energy_for_power function raises an error when given an invalid power unit.
        """
        power: Quantity = Quantity(0.2778, 'kg')
        duration: Quantity = Quantity(1, 'h')
        to_unit: Quantity = Quantity(1, 'kJ')

        with self.assertRaises(ValueError):
            calculate_energy_for_power(power, duration, to_unit)

    def test_calculate_energy_for_power_with_invalid_duration_unit_raises_error(self):
        """
        Tests that the calculate_energy_for_power function raises an error when given an invalid duration unit.
        """
        power: Quantity = Quantity(0.2778, 'kW')
        duration: Quantity = Quantity(1, 'kg')
        to_unit: Quantity = Quantity(1, 'kJ')

        with self.assertRaises(ValueError):
            calculate_energy_for_power(power, duration, to_unit)

    def test_calculate_energy_for_power_with_invalid_energy_unit_raises_error(self):
        """
        Tests that the calculate_energy_for_power function raises an error when given an invalid energy unit.
        """
        power: Quantity = Quantity(0.2778, 'kW')
        duration: Quantity = Quantity(1, 'h')
        to_unit: Quantity = Quantity(1, 'kg')

        with self.assertRaises(ValueError):
            calculate_energy_for_power(power, duration, to_unit)

    def test_convert_to_co2_with_valid_unit_returns_converted_value(self):
        """
        Tests that the convert_to_co2 function returns the converted value when given valid unit.
        """
        
        energy: Quantity = Quantity(1000, 'kWh')

        converted_co2: float = convert_to_co2(energy)

        expected_co2: float = 207.07
        self.assertAlmostEqual(expected_co2, converted_co2, places=4)

    def test_convert_to_co2_with_invalid_energy_unit_raises_error(self):
        """
        Tests that the convert_to_co2 function raises an error when given an invalid energy unit.
        """
        set_application_registry(UNIT_REGISTRY)
        energy: Quantity = Quantity(1000, 'kg')

        with self.assertRaises(ValueError):
            convert_to_co2(energy)

if __name__ == '__main__':
    unittest.main()
