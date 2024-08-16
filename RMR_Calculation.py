def calculate_rmr(gender, weight_kg, height_cm, age):
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
    if gender.lower() == 'male':
        rmr = 88.362 + (13.397 * weight_kg) + (4.799 * height_cm) - (5.677 * age)
    elif gender.lower() == 'female':
        rmr = 447.593 + (9.247 * weight_kg) + (3.098 * height_cm) - (4.330 * age)
    else:
        raise ValueError("Gender must be 'male' or 'female'")

    return rmr

def calculate_dce(rmr, activity_level):
    """
    Calculate the Daily Caloric Expenditure (DCE) based on activity level.

    Parameters:
    - rmr: Resting Metabolic Rate in calories/day
    - activity_level: activity level ('sedentary', 'light', 'moderate', 'very', 'super')

    Returns:
    - dce: Daily Caloric Expenditure in calories/day
    """
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

#Calculate estimated 1 rep max

# Example usage
gender = input("Enter gender (male/female): ").strip()
weight_kg = float(input("Enter weight in kilograms: ").strip())
height_cm = float(input("Enter height in centimeters: ").strip())
age = int(input("Enter age in years: ").strip())
activity_level = input("Enter activity level (sedentary, light, moderate, very, super): ").strip()

rmr = calculate_rmr(gender, weight_kg, height_cm, age)
dce = calculate_dce(rmr, activity_level)

print(f"Resting Metabolic Rate (RMR): {rmr:.2f} calories/day")
print(f"Daily Caloric Expenditure (DCE): {dce:.2f} calories/day")