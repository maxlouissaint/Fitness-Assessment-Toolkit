'''
Module contains functions for common operations
'''

# -------------------------- Conversion functions --------------------------------------
# Convert Pound to Kilo
def convert_Pound2Kilo(weight_lbs):
    return weight_lbs / 2.2046

# Convert Kilo to Pound
def convert_Kilo2Pound(weight_kg):
    return weight_kg * 2.2046

# convert inches to centimeter - return height in centimeter
def convert_Inches2Centimeters(height_in):
    return height_in * 2.54
