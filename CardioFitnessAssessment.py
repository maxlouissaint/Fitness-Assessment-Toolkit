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
def calc_max_HR(age):
    return 220 - age
# ----------------------- Hydration Level Calculation -------------------------------------
def calculate_hydration(weight_kg, activity_minutes):
    base_water = weight_kg * 0.033  # 33 ml per kg
    extra_water = activity_minutes * 0.012  # 12 ml per minute of activity
    return base_water + extra_water

# ----------------------- Heart Rate Zone Calculation --------------------------------------------
def calculate_heart_rate_zones(max_heart_rate):
    zones = {
        'Zone 1': (0.50, 0.60),
        'Zone 2': (0.61, 0.70),
        'Zone 3': (0.71, 0.80),
        'Zone 4': (0.81, 0.90),
        'Zone 5': (0.91, 1.00)
    }
    return {zone: (max_heart_rate * min_val, max_heart_rate * max_val) for zone, (min_val, max_val) in zones.items()}

# ------------------------------ Display Heart Rate Zone -----------------------------
def display_heart_rate_zones(age, rest_heart_rate, gender):
    max_heart_rate = calc_max_HR(age)
    vo2_max = estimate_vo2_max(max_heart_rate, rest_heart_rate, gender)
    heart_rate_zones = calculate_heart_rate_zones(max_heart_rate)
    
    print(f"Estimated VO2 Max: {vo2_max:.2f} mL/kg/min")
    print("Heart Rate Zones:")
    for zone, (min_hr, max_hr) in heart_rate_zones.items():
        print(f"{zone}: {min_hr:.2f} - {max_hr:.2f} bpm")

'''
age = int(input("Enter age: "))
max_heart_rate = calc_max_HR(age)
rest_heart_rate = int(input("Enter resting heart rate:"))
display_heart_rate_zones(age, rest_heart_rate)
'''
