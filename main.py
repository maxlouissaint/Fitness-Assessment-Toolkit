from BodyCompositionAssessment import (
    calculate_body_fat_skinfold,
    estimate_rmr,
    estimate_tdee,
)
from CardioFitnessAssessment import (
    calculate_heart_rate_zones,
    display_heart_rate_zones,
    estimate_max_heart_rate,
    estimate_vo2_max,
)
from DataManipulation import save_to_file
from StrengthAndEnduranceAssessment import (
    estimate_one_rep_max,
    display_training_goals,
)

def collect_user_input():
    age = int(input("Enter age: "))
    gender = input("Enter gender (male/female): ").strip().lower()
    weight = float(input("Enter weight (lbs): "))
    height = float(input("Enter height (inches): "))
    rest_heart_rate = int(input("Enter resting heart rate (BPM): "))
    print(
        "Physical Activity Level (PAL): "
        "1.40-1.69 sedentary/light, "
        "1.70-1.99 active/moderate, "
        "2.00-2.40 vigorous"
    )
    pal = float(input("Enter PAL: "))

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
        pal,
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
        pal,
        measure_one,
        measure_two,
        measure_three,
        weight_lifted,
        reps,
    ) = collect_user_input()

    rmr = estimate_rmr(gender, weight, height, age)
    tdee = estimate_tdee(rmr, pal)
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
    estimated_1rm = estimate_one_rep_max(weight_lifted, reps)

    # Display results
    print(f"Estimated RMR: {rmr:.2f} kcal/day")
    print(f"PAL: {pal:.2f}")
    print(f"Estimated TDEE: {tdee:.2f} kcal/day")
    print(f"Body Fat Percentage: {bf_percent:.2f}%")
    display_heart_rate_zones(age, rest_heart_rate, gender)
    display_training_goals(weight_lifted, reps)

    # Save results
    results = {
        "Estimated RMR (kcal/day)": rmr,
        "Physical Activity Level (PAL)": pal,
        "Estimated TDEE (kcal/day)": tdee,
        "Body Fat %": bf_percent,
        "Estimated VO2 Max (mL/kg/min)": vo2_max,
        "Heart Rate Zones": heart_rate_zones,
        "Estimated 1RM": estimated_1rm,
    }
    save_to_file(results)

if __name__ == "__main__":
    main()
