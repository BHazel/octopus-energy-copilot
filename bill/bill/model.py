"""
Types for working with data extracted from an electricity bill.
"""

class Tariff:
    """
    Represents an electricity tariff.
    """
    def __init__(self,
                 name: str,
                 unit_rate: float,
                 payment_method: str
        ):
        """
        Initialises an instance of the Tariff class.
        """
        self.name = name
        self.unit_rate = unit_rate
        self.payment_method = payment_method

class Usage:
    """
    Represents electricity usage in a bill.
    """
    def __init__(self,
                 consumption: float,
                 cost: float,
                 meter_reading_start: float,
                 meter_reading_end: float
        ):
        """
        Initialises an instance of the Usage class.
        """
        self.consumption = consumption
        self.cost = cost
        self.meter_reading_start = meter_reading_start
        self.meter_reading_end = meter_reading_end

class EnergyBill:
    """
    Represents an energy bill.
    """
    def __init__(self,
                 bill_date: str,
                 supplier: str,
                 distributor: str,
                 property_address: str,
                 usage: Usage,
                 tariff: Tariff
        ):
        """
        Initialises an instance of the EnergyBill class.
        """
        self.bill_date = bill_date
        self.supplier = supplier
        self.distributor = distributor
        self.property_address = property_address
        self.usage = usage
        self.tariff = tariff
