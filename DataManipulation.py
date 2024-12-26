import json

# -------------------- Save Data to File ----------------------------
def save_to_file(data, filename="assessment_results.json"):
    with open(filename, "w") as file:
        json.dump(data, file)

# ----------------------- Reading Data from File ------------------------------
def load_from_file(filename="assessment_results.json"):
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
