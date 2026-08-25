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
from datetime import datetime
from DataManipulation import add_assessment
from StrengthAndEnduranceAssessment import (
    estimate_one_rep_max,
    display_training_goals,
)

def collect_user_input():
    client_id = input("Enter client ID: ").strip()
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
        client_id,
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
        client_id,
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
    if gender == "male":
        skinfolds = {
            "chest": measure_one,
            "abdominal": measure_two,
            "thigh": measure_three,
        }
    else:
        skinfolds = {
            "triceps": measure_one,
            "suprailiac": measure_two,
            "thigh": measure_three,
        }

    assessment = {
        "timestamp": datetime.now().astimezone().isoformat(),
        "inputs": {
            "age": age,
            "gender": gender,
            "weight_lbs": weight,
            "height_in": height,
            "resting_hr_bpm": rest_heart_rate,
            "pal": pal,
            "skinfolds_mm": skinfolds,
            "weight_lifted_lbs": weight_lifted,
            "repetitions": reps,
        },
        "results": {
            "estimated_rmr_kcal_day": rmr,
            "estimated_tdee_kcal_day": tdee,
            "body_fat_percent": bf_percent,
            "estimated_max_heart_rate_bpm": max_heart_rate,
            "estimated_vo2_max_ml_kg_min": vo2_max,
            "heart_rate_zones_bpm": heart_rate_zones,
            "estimated_1rm_lbs": estimated_1rm,
        },
    }

    add_assessment(client_id, assessment)

if __name__ == "__main__":
    main()
