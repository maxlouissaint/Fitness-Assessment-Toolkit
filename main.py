from BodyCompositionAssessment import *
from CardioFitnessAssessment import *
from StrengthAndEnduranceAssessment import *
from DataManipulation import *

def collect_user_input():
    age = int(input("Enter age: "))
    gender = input("Enter gender (male/female): ").strip().lower()
    weight = float(input("Enter weight (lbs): "))
    height = float(input("Enter height (inches): "))
    rest_heart_rate = int(input("Enter resting heart rate (BPM): "))
    activity_level = input("Enter activity level (sedentary, light, moderate, very, super): ").strip().lower()
    return age, gender, weight, height, rest_heart_rate, activity_level

def main():
    # Collect inputs
    age, gender, weight, height, rest_heart_rate, activity_level = collect_user_input()

    # Perform assessments -------- use a switch statement
    rmr = calculate_rmr(gender, weight, height, age)
    dce = calculate_dce(rmr, activity_level)
    bf_percent = calculate_body_fat_skinfold(gender, age, 10, 20, 30)  # Replace with actual measurements
    max_heart_rate = calc_max_HR(age)
    vo2_max = estimate_vo2_max(max_heart_rate, rest_heart_rate, gender)
    heart_rate_zones = calculate_heart_rate_zones(max_heart_rate)
    estimated_1rm = calculate_1RM(200, 8)  # Replace with user inputs

    # Display results
    print(f"RMR: {rmr:.2f} cal/day, DCE: {dce:.2f} cal/day")
    print(f"Body Fat Percentage: {bf_percent:.2f}%")
    display_heart_rate_zones(age, rest_heart_rate, gender)
    display_training_goals(200, 8)  # Replace with actual weight and reps

    # Save results
    results = {
        "RMR": rmr,
        "DCE": dce,
        "Body Fat %": bf_percent,
        "Estimated VO2 Max (mL/kg/min)": vo2_max,
        "Heart Rate Zones": heart_rate_zones,
        "Estimated 1RM": estimated_1rm,
    }
    save_to_file(results)

if __name__ == "__main__":
    main()
