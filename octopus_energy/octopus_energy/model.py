"""
Types for working with data from the Octopus Energy API.
"""

from enum import Enum, Flag

class Consumption:
    """
    Represents consumption data for a given time interval.
    """
    def __init__(self, consumption: float, interval_start, interval_end):
        self.consumption: float = consumption
        self.interval_start: str = interval_start
        self.interval_end: str = interval_end

class ConsumptionGrouping(Enum):
    """
    Defines constants for grouping consumption data.
    """
    HALF_HOUR = None
    HOUR = 'hour'
    DAY = 'day'
    WEEK = 'week'
    MONTH = 'month'
    QUARTER = 'quarter'

class Link:
    """
    Represents a link.
    """
    def __init__(self,
                 href: str,
                 method: str,
                 rel: str):
        self.href: str = href
        self.method: str = method,
        self.rel: str = rel

class Product:
    """
    Represents a product.
    """
    def __init__(self,
                 code: str,
                 full_name: str,
                 display_name: str,
                 description: str,
                 is_variable: bool,
                 is_green: bool,
                 is_tracker: bool,
                 is_prepay: bool,
                 is_business: bool,
                 is_restricted: bool,
                 term: int,
                 available_from: str,
                 available_to: str,
                 links: list[Link],
                 brand: str,
                 tariffs_active_at: str = None,
                 direction: str = None
        ):
        self.code: str = code
        self.full_name: str = full_name
        self.display_name: str = display_name
        self.description: str = description
        self.is_variable: bool = is_variable
        self.is_green: bool = is_green
        self.is_tracker: bool = is_tracker
        self.is_prepay: bool = is_prepay
        self.is_business: bool = is_business
        self.is_restricted: bool = is_restricted
        self.term: int = term
        self.available_from: str = available_from
        self.available_to: str = available_to
        self.links: list[Link] = links
        self.brand: str = brand
        self.tariffs_active_at: str = tariffs_active_at
        self.direction: str = direction

class ProductFiltering(Flag):
    """
    Defines constants for filtering product types.
    """
    DEFAULT = 0
    VARIABLE = 1 << 0
    GREEN = 1 << 1
    TRACKER = 1 << 2
    PREPAY = 1 << 3
    BUSINESS = 1 << 4

class Agreement:
    """
    Represents an agreement.
    """
    def __init__(self,
                 tariff_code: str,
                 valid_from: str,
                 valid_to: str
        ):
        """
        Initialises an instance of the Agreement class.

        Args:
            tariff_code (str): The agreement tariff code.
            valid_from (str): The date the agreement is valid from.
            valid_to (str): The date the agreement is valid to.
        """
        self.tariff_code: str = tariff_code
        self.valid_from: str = valid_from
        self.valid_to: str = valid_to

class Meter:
    """
    Represents a meter.
    """
    def __init__(self,
                 serial_number: str
        ):
        """
        Initialises an instance of the Meter class.

        This is intended as a base class for specific meter types.

        Args:
            serial_number (str): The meter serial number.
        """
        self.serial_number: str = serial_number

class ElectricityMeterRegister:
    """
    Represents an electricity meter register.
    """
    def __init__(self,
                 identifier: str,
                 rate: str,
                 is_settlement_register: bool
        ):
        """
        Initialises an instance of the ElectricityMeterRegister class.

        Args:
            identifier (str): The register identifier.
            rate (str): The register rate.
            is_settlement_register (bool): A value indicating whether the register is a settlement register.
        """
        self.identifier: str = identifier
        self.rate: str = rate
        self.is_settlement_register: bool = is_settlement_register

class ElectricityMeter(Meter):
    """
    Represents an electricity meter.
    """
    def __init__(self,
                 serial_number: str,
                 registers: list[ElectricityMeterRegister]
        ):
        """
        Initialises an instance of the ElectricityMeter class.

        Args:
            serial_number (str): The meter serial number.
            registers (list[ElectricityMeterRegister]): The electricity meter registers.
        """
        Meter.__init__(self, serial_number)
        self.registers: list[ElectricityMeterRegister] = registers

class GasMeter(Meter):
    """
    Represents a gas meter.
    """
    def __init__(self,
                 serial_number: str,
        ):
        """
        Initialises an instance of the GasMeter class.

        Args:
            serial_number (str): The meter serial number.
        """
        Meter.__init__(self, serial_number)

class MeterPoint:
    """
    Represents a meter point.
    """
    def __init__(self,
                 consumption_standard: int = None,
                 meters: list[Meter] = None,
                 agreements: list[Agreement] = None
        ):
        """
        Initialises an instance of the MeterPoint class.

        This is intended as a base class for specific meter point types.

        Args:
            consumption_standard (int, optional): The meter point standard consumption.
                Defaults to None.
            meters (list[Meter], optional): The meters associated with the meter point.
                Defaults to None.
            agreements (list[Agreement], optional): The agreements associated with the meter point.
                Defaults to None.
        """
        self.consumption_standard: int = consumption_standard
        self.meters: list[Meter] = meters
        self.agreements: list[Agreement] = agreements

class ElectricityMeterPoint(MeterPoint):
    """
    Represents an electricity meter point.
    """
    def __init__(self,
                 consumption_standard: int,
                 meters: list[ElectricityMeter],
                 agreements: list[Agreement],
                 mpan: str,
                 profile_class: int,
                 is_export: bool
        ):
        """
        Initialises an instance of the ElectricityMeterPoint class.

        Args:
            consumption_standard (int): The meter point standard consumption.
            meters (list[ElectricityMeter]): The electricity meters associated with the meter point.
            agreements (list[Agreement]): The agreements associated with the meter point.
            mpan (str): The meter point administration number.
            profile_class (int): The meter point profile class.
            is_export (bool): A value indicating whether the meter point is an export meter.
        """
        MeterPoint.__init__(self, consumption_standard, meters, agreements)
        self.mpan: str = mpan
        self.profile_class: int = profile_class
        self.is_export: bool = is_export

class GasMeterPoint(MeterPoint):
    """
    Represents a gas meter point.
    """
    def __init__(self,
                 consumption_standard: int,
                 meters: list[GasMeter],
                 agreements: list[Agreement],
                 mprn: str
        ):
        """
        Initialises an instance of the GasMeterPoint class.

        Args:
            consumption_standard (int): The meter point standard consumption.
            meters (list[GasMeter]): The gas meters associated with the meter point.
            agreements (list[Agreement]): The agreements associated with the meter point.
            mprn (str): The meter point registration number.
        """
        MeterPoint.__init__(self, consumption_standard, meters, agreements)
        self.mprn: str = mprn

class Property:
    """
    Represents a property.
    """
    def __init__(self,
                 moved_in_at: str,
                 moved_out_at: str = None,
                 address_line_1: str = None,
                 address_line_2: str = None,
                 address_line_3: str = None,
                 town: str = None,
                 county: str = None,
                 postcode: str = None,
                 electricity_meter_points: list[ElectricityMeterPoint] = None,
                 gas_meter_points: list[GasMeterPoint] = None
        ):
        """
        Initialises an instance of the Property class.
        
        Args:
            moved_in_at (str): The date the account holder moved into the property.
            moved_out_at (str, optional): The date the account holder moved out of the property.
                Defaults to None.
            address_line_1 (str, optional): The first line of the property address.
                Defaults to None.
            address_line_2 (str, optional): The second line of the property address.
                Defaults to None.
            address_line_3 (str, optional): The third line of the property address.
                Defaults to None.
            town (str, optional): The town of the property address.
                Defaults to None.
            county (str, optional): The county of the property address.
                Defaults to None.
            postcode (str, optional): The post code of the property address.
                Defaults to None.
            electricity_meter_points (list[ElectricityMeterPoint], optional): The electricity meter points associated with the property.
                Defaults to None.
            gas_meter_points (list[GasMeterPoint], optional): The gas meter points associated with the property.
                Defaults to None.
        """
        self.moved_in_at: str = moved_in_at
        self.moved_out_at: str = moved_out_at
        self.address_line_1: str = address_line_1
        self.address_line_2: str = address_line_2
        self.address_line_3: str = address_line_3
        self.town: str = town
        self.county: str = county
        self.postcode: str = postcode
        self.electricity_meter_points: list[ElectricityMeterPoint] = electricity_meter_points
        self.gas_meter_points: list[GasMeterPoint] = gas_meter_points

class Account:
    """
    Represents an account.
    """
    def __init__(self,
                 number: str,
                 properties: list[Property]
        ):
        """
        Initialises an instance of the Account class.
        
        Args:
            number (str): The account number.
            properties (list[Property]): The properties associated with the account.
        """
        self.number: str = number
        self.properties: list[Property] = properties
