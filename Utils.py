'''
Module contains functions for common operations
'''

# -------------------------- Conversion functions --------------------------------------
# Convert Pound to Kilo
def pounds_to_kilograms(weight_lbs):
    return weight_lbs / 2.2046

# Convert Kilo to Pound
def kilograms_to_pounds(weight_kg):
    return weight_kg * 2.2046

# convert inches to centimeter - return height in centimeter
def inches_to_centimeters(height_in):
    return height_in * 2.54
