
# Import necessary modules
import math
from Utils import * # import conversion functions

# ---------------------------- Skinfold Body Fat Calculation --------------------------------------
"""
    Calculate body fat using skinfold equation
    
    Parameters:
    - gender: 'male' or 'female'
    - measureOne: measurement from location 1
    - measureTwo: measurement from location 2
    - measureThree: measurement from location 3

    Returns:
    - bf_percent: body fat percentage using skinfold
"""
def calculate_body_fat_skinfold(gender, age, measureOne, measureTwo, measureThree):
    """
    Estimate body-fat percentage using the Jackson-Pollock three-site
    body-density equations and the Siri density-to-fat conversion.

    Study age ranges:
        male:   18-61 years
        female: 18-55 years

    Skinfold measurements are expected in millimeters.
    """
    gender = gender.strip().lower()

    if gender not in ("male", "female"):
        raise ValueError("Gender must be 'male' or 'female'.")

    if not isinstance(age, (int, float)) or isinstance(age, bool):
        raise ValueError("Age must be numeric.")

    if not math.isfinite(age):
        raise ValueError("Age must be finite.")

    age_limits = {
        "male": (18, 61),
        "female": (18, 55),
    }

    minimum_age, maximum_age = age_limits[gender]

    if age < minimum_age or age > maximum_age:
        raise ValueError(
            f"Age for the {gender} Jackson-Pollock equation must be "
            f"between {minimum_age} and {maximum_age} years."
        )

    measurements = (measureOne, measureTwo, measureThree)

    for measurement in measurements:
        if not isinstance(measurement, (int, float)) or isinstance(measurement, bool):
            raise ValueError("Skinfold measurements must be numeric.")

        if not math.isfinite(measurement):
            raise ValueError("Skinfold measurements must be finite.")

        if measurement <= 0:
            raise ValueError(
                "Skinfold measurements must be greater than zero."
            )

    sum_skinfold = sum(measurements)

    if gender == "male":
        body_density = (
            1.10938
            - (0.0008267 * sum_skinfold)
            + (0.0000016 * (sum_skinfold ** 2))
            - (0.0002574 * age)
        )
    else:
        body_density = (
            1.0994921
            - (0.0009929 * sum_skinfold)
            + (0.0000023 * (sum_skinfold ** 2))
            - (0.0001392 * age)
        )

    if not math.isfinite(body_density) or body_density <= 0:
        raise ValueError(
            "Inputs produced an invalid estimated body density."
        )

    bf_percent = ((4.95 / body_density) - 4.50) * 100

    if not math.isfinite(bf_percent) or not 0 <= bf_percent <= 100:
        raise ValueError(
            "Inputs produced an invalid estimated body-fat percentage."
        )

    return bf_percent


# -------------------------- Resting Metabolid Rate Calculation ------------------------------------------------
"""
    Calculate the Resting Metabolic Rate (RMR) using the Harris-Benedict equation.

    Parameters:
    - gender: 'male' or 'female'
    - weight_kg: weight in kilograms
    - height_cm: height in centimeters
    - age: age in years

    Returns:
    - rmr: Resting Metabolic Rate in calories/day
    """
def calculate_rmr(gender, weight_lbs, height_in, age):
    
    height_cm = convert_Inches2Centimeters(height_in)
    weight_kg = convert_Pound2Kilo(weight_lbs)

    if gender.lower() == 'male':
        rmr = 88.362 + (13.397 * weight_kg) + (4.799 * height_cm) - (5.677 * age)
    elif gender.lower() == 'female':
        rmr = 447.593 + (9.247 * weight_kg) + (3.098 * height_cm) - (4.330 * age)
    else:
        raise ValueError("Gender must be 'male' or 'female'")

    return rmr

# ---------------------- Daily Caloric Exxpenditure Calculation ----------------------------------
"""
    Calculate the Daily Caloric Expenditure (DCE) based on activity level.

    Parameters:
    - rmr: Resting Metabolic Rate in calories/day
    - activity_level: activity level ('sedentary', 'light', 'moderate', 'very', 'super')

    Returns:
    - dce: Daily Caloric Expenditure in calories/day
    """
def calculate_dce(rmr, activity_level):
    
    activity_factors = {
        'sedentary': 1.2,
        'light': 1.375,
        'moderate': 1.55,
        'very': 1.725,
        'super': 1.9
    }

    if activity_level.lower() not in activity_factors:
        raise ValueError("Activity level must be one of 'sedentary', 'light', 'moderate', 'very', or 'super'")

    dce = rmr * activity_factors[activity_level.lower()]
    return dce