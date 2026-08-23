# ---------------------- 1-Rep Max Calculation ------------------------
def calculate_1RM(weight_lifted, reps):
    """
    Estimate one-repetition maximum using the Epley equation.

    For a true single repetition, the observed weight is returned directly.
    For sets of 2 to 10 repetitions:

        estimated_1rm = weight_lifted * (1 + reps / 30)

    Higher-repetition sets are rejected because 1RM prediction becomes less
    useful as muscular endurance contributes more heavily to performance.
    """
    if weight_lifted <= 0:
        raise ValueError("Weight lifted must be greater than zero.")

    if not isinstance(reps, int) or isinstance(reps, bool):
        raise ValueError("Repetitions must be an integer.")

    if reps < 1 or reps > 10:
        raise ValueError("Repetitions must be between 1 and 10.")

    if reps == 1:
        return float(weight_lifted)

    return weight_lifted * (1 + reps / 30)

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