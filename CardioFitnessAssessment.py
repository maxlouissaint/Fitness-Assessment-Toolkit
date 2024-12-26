# Measure resting heart rate (RHR)
# --------------- Heart Rate Baed V02_max -------------------------------------------
def calculate_vo2_max(max_heart_rate, rest_heart_rate):
    return max_heart_rate / rest_heart_rate #returns estimated VO2_max

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
def display_heart_rate_zones(age, rest_heart_rate):
    max_heart_rate = calc_max_HR(age)
    vo2_max = calculate_vo2_max(max_heart_rate, rest_heart_rate)
    heart_rate_zones = calculate_heart_rate_zones(max_heart_rate)
    
    print(f"VO2 Max: {vo2_max:.2f}")
    print("Heart Rate Zones:")
    for zone, (min_hr, max_hr) in heart_rate_zones.items():
        print(f"{zone}: {min_hr:.2f} - {max_hr:.2f} bpm")

'''
age = int(input("Enter age: "))
max_heart_rate = calc_max_HR(age)
rest_heart_rate = int(input("Enter resting heart rate:"))
display_heart_rate_zones(age, rest_heart_rate)
'''
