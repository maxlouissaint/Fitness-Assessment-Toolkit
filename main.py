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
    activity_level = input(
        "Enter activity level (sedentary, light, moderate, very, super): "
    ).strip().lower()

    if gender == "male":
        print("Enter skinfold measurements in millimeters:")
        measure_one = float(input("Chest: "))
        measure_two = float(input("Abdominal: "))
        measure_three = float(input("Thigh: "))
    elif gender == "female":
        print("Enter skinfold measurements in millimeters:")
        measure_one = float(input("Triceps: "))
        measure_two = float(input("Suprailiac: "))
        measure_three = float(input("Thigh: "))
    else:
        raise ValueError("Gender must be 'male' or 'female'.")

    weight_lifted = float(
        input("Enter weight lifted for strength assessment (lbs): ")
    )
    reps = int(input("Enter repetitions completed: "))

    return (
        age,
        gender,
        weight,
        height,
        rest_heart_rate,
        activity_level,
        measure_one,
        measure_two,
        measure_three,
        weight_lifted,
        reps,
    )

def main():
    # Collect inputs
    (
        age,
        gender,
        weight,
        height,
        rest_heart_rate,
        activity_level,
        measure_one,
        measure_two,
        measure_three,
        weight_lifted,
        reps,
    ) = collect_user_input()

    # Perform assessments -------- use a switch statement
    rmr = calculate_rmr(gender, weight, height, age)
    dce = calculate_dce(rmr, activity_level)
    bf_percent = calculate_body_fat_skinfold(
        gender,
        age,
        measure_one,
        measure_two,
        measure_three,
    )
    max_heart_rate = estimate_max_heart_rate(age)
    vo2_max = estimate_vo2_max(max_heart_rate, rest_heart_rate, gender)
    heart_rate_zones = calculate_heart_rate_zones(max_heart_rate)
    estimated_1rm = calculate_1RM(weight_lifted, reps)

    # Display results
    print(f"RMR: {rmr:.2f} cal/day, DCE: {dce:.2f} cal/day")
    print(f"Body Fat Percentage: {bf_percent:.2f}%")
    display_heart_rate_zones(age, rest_heart_rate, gender)
    display_training_goals(weight_lifted, reps)

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
