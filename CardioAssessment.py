
def calculate_vo2_max(max_heart_rate, rest_heart_rate):
    return max_heart_rate / rest_heart_rate #returns estimated VO2_max

max_heart_rate = int(input("Enter max heart rate (220 - age):"))
rest_heart_rate = int(input("Enter resting heart rate:"))

zone_range = {
    'Zone 1': (0.5, 0.60),
    'Zone 2': (0.61, 0.70),
    'Zone 3': (0.71, 0.80),
    'Zone 4': (0.81, 0.90),
    'Zone 5': (0.91, 1.00)
    }

zone1_max = zone_range['Zone 1'][1]
zone1_min = zone_range['Zone 1'][0]
zone2_max = zone_range['Zone 2'][1]
zone2_min = zone_range['Zone 2'][0]
zone3_max = zone_range['Zone 3'][1]
zone3_min = zone_range['Zone 3'][0]
zone4_max = zone_range['Zone 4'][1]
zone4_min = zone_range['Zone 4'][0]
zone5_max = zone_range['Zone 5'][1]
zone5_min = zone_range['Zone 5'][0]


print('Heart Rate Zone Range:')
print(f"Zone 1 (50-60% of Max HR):\n     Max: {max_heart_rate * zone1_max:.2f}      Min: {max_heart_rate * zone1_max:.2f}\n")
print(f"Zone 2 (61-70% of Max HR):\n     Max: {max_heart_rate * zone2_max:.2f}    Min: {max_heart_rate * zone2_min:.2f}\n")
print(f"Zone 3 (71-80% of Max HR):\n     Max: {max_heart_rate * zone3_max:.2f}    Min: {max_heart_rate * zone3_min:.2f}\n")
print(f"Zone 4 (81-90% of Max HR):\n     Max: {max_heart_rate * zone4_max:.2f}    Min: {max_heart_rate * zone4_min:.2f}\n")
print(f"Zone 5 (91-100% of Max HR):\n     Max: {max_heart_rate * zone5_max:.2f}    Min: {max_heart_rate * zone5_min:.2f}\n")