
# Import necessary modules
import math
from Utils import inches_to_centimeters, pounds_to_kilograms # import conversion functions

# ---------------------------- Skinfold Body Fat Calculation --------------------------------------
"""
    Calculate body fat using skinfold equation
    
    Parameters:
    - gender: 'male' or 'female'
    - measure_one: measurement from location 1
    - measure_two: measurement from location 2
    - measure_three: measurement from location 3

    Returns:
    - bf_percent: body fat percentage using skinfold
"""
def calculate_body_fat_skinfold(gender, age, measure_one, measure_two, measure_three):
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

    measurements = (measure_one, measure_two, measure_three)

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
def estimate_rmr(gender, weight_lbs, height_in, age):
    """
    Estimate resting metabolic rate using the revised Harris-Benedict
    equations published by Roza and Shizgal (1984).

    Inputs:
        gender: "male" or "female"
        weight_lbs: body weight in pounds
        height_in: height in inches
        age: age in years

    Returns:
        Estimated resting energy expenditure in kcal/day.

    This is a population-derived estimate, not a direct metabolic
    measurement.
    """
    gender = gender.strip().lower()

    if gender not in ("male", "female"):
        raise ValueError("Gender must be 'male' or 'female'.")

    values = {
        "weight": weight_lbs,
        "height": height_in,
        "age": age,
    }

    for name, value in values.items():
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            raise ValueError(f"{name.capitalize()} must be numeric.")

        if not math.isfinite(value):
            raise ValueError(f"{name.capitalize()} must be finite.")

        if value <= 0:
            raise ValueError(f"{name.capitalize()} must be greater than zero.")

    height_cm = inches_to_centimeters(height_in)
    weight_kg = pounds_to_kilograms(weight_lbs)

    if gender == "male":
        rmr = (
            88.362
            + (13.397 * weight_kg)
            + (4.799 * height_cm)
            - (5.677 * age)
        )
    else:
        rmr = (
            447.593
            + (9.247 * weight_kg)
            + (3.098 * height_cm)
            - (4.330 * age)
        )

    if not math.isfinite(rmr) or rmr <= 0:
        raise ValueError(
            "Inputs produced an invalid resting metabolic rate estimate."
        )

    return rmr


# ---------------------- Total Daily Energy Expenditure ----------------------

def estimate_tdee(rmr, pal):
    """
    Estimate total daily energy expenditure from resting metabolic rate
    and Physical Activity Level (PAL).

        estimated TDEE = RMR * PAL

    PAL represents total daily energy expenditure as a multiple of resting
    energy expenditure.

    Habitual adult lifestyle ranges used as guidance:
        1.40-1.69: sedentary or light activity
        1.70-1.99: active or moderately active
        2.00-2.40: vigorous or vigorously active

    Returns:
        Estimated total daily energy expenditure in kcal/day.
    """
    if not isinstance(rmr, (int, float)) or isinstance(rmr, bool):
        raise ValueError("RMR must be numeric.")

    if not math.isfinite(rmr):
        raise ValueError("RMR must be finite.")

    if rmr <= 0:
        raise ValueError("RMR must be greater than zero.")

    if not isinstance(pal, (int, float)) or isinstance(pal, bool):
        raise ValueError("PAL must be numeric.")

    if not math.isfinite(pal):
        raise ValueError("PAL must be finite.")

    if pal < 1.40 or pal > 2.40:
        raise ValueError(
            "PAL must be between 1.40 and 2.40 for this assessment."
        )

    tdee = rmr * pal

    if not math.isfinite(tdee) or tdee <= 0:
        raise ValueError(
            "Inputs produced an invalid total daily energy expenditure estimate."
        )

    return tdee
