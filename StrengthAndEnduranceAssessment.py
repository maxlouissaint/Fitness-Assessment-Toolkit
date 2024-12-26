# ---------------------- 1-Rep Max Calculation ------------------------
def calculate_1RM(weight_lifted, numOfRep):
    estimated_percent_of_1RM = (100 - (numOfRep * 2.5)) / 100
    return weight_lifted / estimated_percent_of_1RM #estimated 1RM

# ---------------------- Training Intensity Ranges ----------------------------------
# Training intensity ranges
def calculate_training_intensities(estimated_1rm):
    intensity_ranges = {
        'Endurance': (0, 0.66),
        'Hypertrophy': (0.67, 0.85),
        'Strength': (0.86, 1.00),
        'Power (Single-Rep)': (0.80, 0.90),
        'Power (Multi-Rep)': (0.75, 0.85)
    }
    return {goal: (estimated_1rm * min_val, estimated_1rm * max_val) for goal, (min_val, max_val) in intensity_ranges.items()}

# ------------------------- Display Training Goals -----------------------------
def display_training_goals(weight_lifted, reps):
    estimated_1rm = calculate_1RM(weight_lifted, reps)
    print(f"Estimated 1RM: {estimated_1rm:.2f} lbs")
    
    training_intensities = calculate_training_intensities(estimated_1rm)
    print("Training Intensity Ranges:")
    for goal, (min_weight, max_weight) in training_intensities.items():
        print(f"{goal}: {min_weight:.2f} - {max_weight:.2f} lbs")

# display_training_goals(10, 5)