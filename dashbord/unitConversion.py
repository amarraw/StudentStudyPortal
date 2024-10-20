conversion_factors = {
    'meters_kilometers': 0.001,
    'meters_centimeters': 100,
    'meters_inches': 39.37,
    'meters_feet': 3.281,
    'kilometers_meters': 1000,
    'centimeters_meters': 0.01,
    'inches_meters': 0.0254,
    'feet_meters': 0.3048,
}


def convert_units(value, from_unit, to_unit):
    if from_unit == to_unit:
        return value 
    key = f'{from_unit}_{to_unit}'
    return value * conversion_factors.get(key, 1)  