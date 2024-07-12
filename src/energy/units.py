"""
Defines constants for energy units.
"""

from energy import UNIT_REGISTRY

# Duration
s = UNIT_REGISTRY.second
min = UNIT_REGISTRY.minute
hr = UNIT_REGISTRY.hour

# Energy
cal = UNIT_REGISTRY.calorie
eV = UNIT_REGISTRY.electron_volt
J = UNIT_REGISTRY.joule
kJ = UNIT_REGISTRY.kilojoule
MJ = UNIT_REGISTRY.megajoule
Wh = UNIT_REGISTRY.watt_hour
kWh = UNIT_REGISTRY.kilowatt_hour
MWh = UNIT_REGISTRY.megawatt_hour

# Mass
kg = UNIT_REGISTRY.kilogram
tonne = UNIT_REGISTRY.tonne

# Power
hp = UNIT_REGISTRY.horsepower
W = UNIT_REGISTRY.watt
kW = UNIT_REGISTRY.kilowatt
MW = UNIT_REGISTRY.megawatt

DURATION_UNITS = [
    's', 'sec', 'second',
    'm', 'min', 'minute',
    'h', 'hr', 'hour'
]

DURATION_UNIT_MAP = {
    's': s,
    'sec': s,
    'second': s,
    'm': min,
    'min': min,
    'minute': min,
    'h': hr,
    'hr': hr,
    'hour': hr,
}

ENERGY_UNITS = [
    'cal', 'calorie',
    'ev', 'eV', 'electronvolt',
    'j', 'J', 'joule',
    'kj', 'kJ', 'kilojoule',
    'mj', 'MJ', 'megajoule',
    'wh', 'Wh', 'watt-hour',
    'kwh', 'kWh', 'kilowatt-hour',
    'mwh', 'MWh', 'megawatt-hour',
]

ENERGY_UNIT_MAP = {
    'cal': cal,
    'calorie': cal,
    'ev': eV,
    'electronvolt': eV,
    'j': J,
    'kj': kJ,
    'mj': MJ,
    'wh': Wh,
    'kwh': kWh,
    'mwh': MWh,
}

POWER_UNITS = [
    'hp', 'horsepower',
    'w', 'W', 'watt',
    'kw', 'kW', 'kilowatt',
    'mw', 'MW', 'megawatt',
]

POWER_UNIT_MAP = {
    'hp': hp,
    'w': W,
    'kw': kW,
    'mw': MW,
}
