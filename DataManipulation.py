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

# ----------------------- Writing Assessment Log ------------------------------
def add_assessment(
    client_id,
    assessment,
    filename="assessment_results.json",
):
    if not isinstance(client_id, str):
        raise TypeError("Client ID must be a string.")

    if not client_id.strip():
        raise ValueError("Client ID cannot be empty.")

    data = load_from_file(filename)

    if "clients" not in data:
        data["clients"] = {}

    if client_id not in data["clients"]:
        data["clients"][client_id] = {
            "assessments": []
        }

    data["clients"][client_id]["assessments"].append(
        assessment
    )

    save_to_file(data, filename)
