# Measure resting heart rate (RHR)
# --------------- Heart Rate Baed V02_max -------------------------------------------
def estimate_vo2_max(max_heart_rate, rest_heart_rate, gender):
    """
    Estimate mass-specific VO2 max using the Heart Rate Ratio Method.

    Published proportionality factors used by this implementation:
        male:   15.3
        female: 14.5

    The estimate is calculated as:

        VO2 max = proportionality_factor * (HRmax / HRrest)

    These factors were derived from trained study populations. The result is
    therefore an indirect fitness estimate, not a direct VO2 max measurement,
    and accuracy can vary by population.

    Returns:
        Estimated VO2 max in mL/kg/min.
    """
    if max_heart_rate <= 0:
        raise ValueError("Maximum heart rate must be greater than zero.")

    if rest_heart_rate <= 0:
        raise ValueError("Resting heart rate must be greater than zero.")

    if rest_heart_rate >= max_heart_rate:
        raise ValueError("Resting heart rate must be lower than maximum heart rate.")

    factors = {
        "male": 15.3,
        "female": 14.5,
    }

    gender = gender.strip().lower()

    if gender not in factors:
        raise ValueError("Gender must be 'male' or 'female'.")

    return factors[gender] * (max_heart_rate / rest_heart_rate)


# -------------------------- Maximum Heart Rate Calculation ----------------------------------------
def estimate_max_heart_rate(age):
    """
    Estimate maximum heart rate using the Tanaka age-prediction equation.

        estimated HRmax = 208 - (0.7 * age)

    This is a population-derived estimate for healthy adults, not a measured
    maximum heart rate. Individual values can differ substantially from the
    prediction.
    """
    if not isinstance(age, (int, float)) or isinstance(age, bool):
        raise ValueError("Age must be numeric.")

    if age < 18:
        raise ValueError(
            "The Tanaka maximum-heart-rate estimate is intended for adults."
        )

    max_heart_rate = 208 - (0.7 * age)

    if max_heart_rate <= 0:
        raise ValueError(
            "Age produced an invalid estimated maximum heart rate."
        )

    return max_heart_rate

# ----------------------- Heart Rate Zone Calculation --------------------------------------------
def calculate_heart_rate_zones(max_heart_rate):
    """
    Calculate five continuous training zones as percentages of maximum
    heart rate.

    Zone 1: 50-60%
    Zone 2: 60-70%
    Zone 3: 70-80%
    Zone 4: 80-90%
    Zone 5: 90-100%
    """
    if max_heart_rate <= 0:
        raise ValueError("Maximum heart rate must be greater than zero.")

    zones = {
        "Zone 1": (0.50, 0.60),
        "Zone 2": (0.60, 0.70),
        "Zone 3": (0.70, 0.80),
        "Zone 4": (0.80, 0.90),
        "Zone 5": (0.90, 1.00),
    }

    return {
        zone: (
            max_heart_rate * min_value,
            max_heart_rate * max_value,
        )
        for zone, (min_value, max_value) in zones.items()
    }

# ------------------------------ Display Heart Rate Zone -----------------------------
def display_heart_rate_zones(age, rest_heart_rate, gender):
    max_heart_rate = estimate_max_heart_rate(age)
    vo2_max = estimate_vo2_max(max_heart_rate, rest_heart_rate, gender)
    heart_rate_zones = calculate_heart_rate_zones(max_heart_rate)
    
    print(f"Estimated VO2 Max: {vo2_max:.2f} mL/kg/min")
    print("Heart Rate Zones:")
    for zone, (min_hr, max_hr) in heart_rate_zones.items():
        print(f"{zone}: {min_hr:.2f} - {max_hr:.2f} bpm")
