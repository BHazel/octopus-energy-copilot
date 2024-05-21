"""
Types for working with data from the Octopus Energy API.
"""

from enum import Enum

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
