def calculate_1RM(weight_lifted, numOfRep):
    estimated_percent_of_1RM = (100 - (numOfRep * 2.5)) / 100
    return weight_lifted / estimated_percent_of_1RM #estimated 1RM

training_goal = {
    'Endurance': (0, 0.66),
    'Hypertrophy': (0.67, 0.85),
    'Strength': (0.86, 1),
    'Power Single-Rep': (0.80, 0.90),
    'Power Multi-Rep': (0.75, 0.85)
    }

hypertrophy_max = training_goal['Hypertrophy'][1]
hypertrophy_min = training_goal['Hypertrophy'][0]
strength_max = training_goal['Strength'][1]
strength_min = training_goal['Strength'][0]
power_single_max = training_goal['Power Single-Rep'][1]
power_single_min = training_goal['Power Single-Rep'][0]
power_multi_max = training_goal['Power Multi-Rep'][1]
power_multi_min = training_goal['Power Multi-Rep'][0]



#def calculate_resTraining_intensity()
    


def print_result():
    weight_lifted = int(input("Enter weight lifted in lbs: ").strip())
    numOfRep = int(input("Enter number of reps: ").strip())

    estimated_1RM = calculate_1RM(weight_lifted, numOfRep)
    print(f"Estimated 1RM: {estimated_1RM:.2f}")

    print('Weight Range Per Intensity:')
    print(f"Endurance (Below 67% 1RM):\n     Max: {estimated_1RM * .67:.2f}\n")
    print(f"Hypertrophy (67-85% 1RM):\n     Max: {estimated_1RM * hypertrophy_max:.2f}    Min: {estimated_1RM * hypertrophy_min:.2f}\n")
    print(f"Strength (Greater than 85% 1RM):\n     Max: {estimated_1RM * strength_max:.2f}    Min: {estimated_1RM * strength_min:.2f}\n")
    print(f"Power-Single Rep (80-90% 1RM):\n     Max: {estimated_1RM * power_single_max:.2f}    Min: {estimated_1RM * power_single_min:.2f}\n")
    print(f"Power-Multi Rep (75-85% 1RM):\n     Max: {estimated_1RM * power_multi_max:.2f}    Min: {estimated_1RM * power_multi_min:.2f}\n")


print_result()