# Fitness Assessment Toolkit

A modular Python command-line application for calculating and storing fitness-related assessment estimates using published equations, input validation, unit testing, and persistent client assessment history.

The project began as a small collection of fitness calculation scripts and has been refactored into a more structured software toolkit with separated calculation modules, validation logic, automated tests, and JSON-based persistence.

> This project is intended for educational and software-engineering purposes. Calculated values are estimates and are not substitutes for laboratory measurement, medical evaluation, diagnosis, or individualized professional guidance.

---

## Overview

The Fitness Assessment Toolkit currently supports estimation of:

- Resting Metabolic Rate (RMR)
- Total Daily Energy Expenditure (TDEE)
- Body-fat percentage from three-site skinfold measurements
- Age-predicted maximum heart rate
- Heart-rate training zones
- Estimated VO₂max using the heart-rate-ratio method
- Estimated one-repetition maximum (1RM)
- Percentage-based training-intensity ranges
- Historical assessment storage for multiple anonymous clients

The application is designed as a command-line workflow:

~~~text
User Inputs
    ↓
Input Validation
    ↓
Fitness Calculations
    ↓
Displayed Results
    ↓
Assessment Record
    ↓
JSON Persistence
~~~

---

## Project Goals

The primary goals of the project are to:

- implement published fitness-estimation equations in Python,
- separate fitness calculations into focused modules,
- validate inputs before calculations are performed,
- distinguish published equations from application-specific design choices,
- verify expected behavior through automated unit tests,
- preserve repeated assessments instead of overwriting previous results,
- maintain a clear data structure for historical assessment records,
- provide a foundation for future integration with fitness decision-support models.

---

## Current Features

### Metabolic Assessment

The toolkit estimates resting metabolic rate using the revised Harris–Benedict equations.

It then estimates total daily energy expenditure using:

~~~text
TDEE = Estimated RMR × Physical Activity Level
~~~

The application currently supports PAL values between:

~~~text
1.40 and 2.40
~~~

---

### Body-Composition Assessment

Body-fat percentage is estimated using sex-specific Jackson–Pollock three-site skinfold equations.

For men:

~~~text
Chest
Abdominal
Thigh
~~~

For women:

~~~text
Triceps
Suprailiac
Thigh
~~~

The resulting estimated body density is converted to body-fat percentage using the Siri equation.

The implementation also validates the supported age ranges for the equations.

---

### Cardiovascular Assessment

The toolkit estimates maximum heart rate using the Tanaka equation:

~~~text
HRmax = 208 - (0.7 × age)
~~~

Estimated HRmax is then used to calculate five percentage-based heart-rate zones:

~~~text
Zone 1: 50–60% HRmax
Zone 2: 60–70% HRmax
Zone 3: 70–80% HRmax
Zone 4: 80–90% HRmax
Zone 5: 90–100% HRmax
~~~

These zones are currently treated as a toolkit implementation convention rather than individualized physiological thresholds.

---

### Estimated VO₂max

The toolkit estimates VO₂max using the heart-rate-ratio method.

Conceptually:

~~~text
Estimated HRmax
      ↓
HRmax / Resting HR
      ↓
Sex-specific proportionality factor
      ↓
Estimated VO₂max
~~~

The implementation currently uses:

~~~text
Male:   15.3 × (HRmax / HRrest)
Female: 14.5 × (HRmax / HRrest)
~~~

Output is expressed in:

~~~text
mL·kg⁻¹·min⁻¹
~~~

This is an indirect estimate and should not be interpreted as equivalent to directly measured VO₂max.

---

### Strength Assessment

Estimated one-repetition maximum is calculated using the Epley equation:

~~~text
Estimated 1RM = weight_lifted × (1 + repetitions / 30)
~~~

For an actual one-repetition set:

~~~text
1 repetition → observed weight is returned directly
~~~

The toolkit currently accepts sets from:

~~~text
1–10 repetitions
~~~

The repetition restriction is an application design decision intended to limit estimation at higher repetition counts.

---

### Training-Intensity Ranges

The current application also displays percentage-based training ranges for:

- endurance,
- hypertrophy,
- strength,
- single-repetition power,
- multi-repetition power.

These ranges remain part of the current implementation.

However, the project does **not currently claim that the specific percentage boundaries have been independently validated within this repository**.

They should currently be interpreted as provisional application behavior rather than as one of the literature-backed estimation methods described in the project references.

---

## Assessment History

Earlier versions of the application saved only the most recent result.

The current persistence model supports:

- multiple clients,
- multiple assessments per client,
- append-only assessment history,
- preservation of both assessment inputs and calculated results.

Each client is identified using an anonymous caller-supplied identifier such as:

~~~text
client_001
client_002
~~~

The application does not require names, email addresses, or other identifying profile information.

---

## Data Structure

Assessment data is stored in JSON.

The high-level structure is:

~~~text
data
└── clients
    ├── client_001
    │   └── assessments
    │       ├── assessment 1
    │       ├── assessment 2
    │       └── ...
    │
    └── client_002
        └── assessments
            └── assessment 1
~~~

Each assessment contains three primary sections:

~~~text
assessment
├── timestamp
├── inputs
└── results
~~~

Example:

~~~json
{
  "clients": {
    "client_001": {
      "assessments": [
        {
          "timestamp": "2026-08-24T19:26:37.735387-04:00",
          "inputs": {
            "age": 30,
            "gender": "male",
            "weight_lbs": 180.0,
            "height_in": 70.0,
            "resting_hr_bpm": 60,
            "pal": 1.75,
            "skinfolds_mm": {
              "chest": 10.0,
              "abdominal": 20.0,
              "thigh": 30.0
            },
            "weight_lifted_lbs": 200.0,
            "repetitions": 8
          },
          "results": {
            "estimated_rmr_kcal_day": 1865.1452804681123,
            "estimated_tdee_kcal_day": 3264.0042408191966,
            "body_fat_percent": 17.94527592700428,
            "estimated_max_heart_rate_bpm": 187.0,
            "estimated_vo2_max_ml_kg_min": 47.685,
            "heart_rate_zones_bpm": {
              "Zone 1": [93.5, 112.2],
              "Zone 2": [112.2, 130.9],
              "Zone 3": [130.9, 149.6],
              "Zone 4": [149.6, 168.3],
              "Zone 5": [168.3, 187.0]
            },
            "estimated_1rm_lbs": 253.33333333333331
          }
        }
      ]
    }
  }
}
~~~

Calculated values are stored at full precision. Formatting and rounding are applied only when results are displayed to the user.

---

## Append-Only Persistence

When a new assessment is saved for an existing client, the toolkit appends the assessment to that client's history.

Conceptually:

~~~text
Existing data
    ↓
Find "clients"
    ↓
Find client_id
    ↓
Find "assessments"
    ↓
Append new assessment
    ↓
Save updated JSON
~~~

In Python:

~~~python
data["clients"][client_id]["assessments"].append(assessment)
~~~

This preserves historical assessment records rather than replacing them.

The generated file:

~~~text
assessment_results.json
~~~

is excluded from Git tracking so locally generated assessment data is not published with the repository.

---

## Project Structure

~~~text
Fitness-Assessment-Toolkit/
├── BodyCompositionAssessment.py
├── CardioFitnessAssessment.py
├── DataManipulation.py
├── StrengthAndEnduranceAssessment.py
├── Utils.py
├── main.py
├── docs/
│   └── references.md
├── tests/
│   ├── test_body_composition.py
│   ├── test_cardio.py
│   ├── test_persistence.py
│   ├── test_strength.py
│   └── test_utils.py
├── .gitignore
└── README.md
~~~

### Module Responsibilities

`BodyCompositionAssessment.py`

~~~text
RMR estimation
TDEE estimation
Skinfold body-fat estimation
~~~

`CardioFitnessAssessment.py`

~~~text
Maximum heart-rate estimation
Heart-rate zones
Heart-rate-ratio VO₂max estimation
~~~

`StrengthAndEnduranceAssessment.py`

~~~text
Estimated 1RM
Training-intensity ranges
~~~

`DataManipulation.py`

~~~text
JSON file loading
JSON file saving
Client assessment-history persistence
~~~

`Utils.py`

~~~text
Unit conversions
~~~

`main.py`

~~~text
CLI input collection
Calculation orchestration
Result display
Assessment-record construction
Persistence integration
~~~

---

## Automated Testing

The project uses Python's built-in `unittest` framework.

The current test suite contains **52 automated tests** covering:

- unit conversions,
- RMR calculations,
- TDEE calculations,
- body-fat calculations,
- supported body-fat age boundaries,
- invalid skinfold inputs,
- maximum heart-rate estimation,
- VO₂max estimation,
- heart-rate-zone continuity,
- 1RM estimation,
- repetition boundaries,
- invalid numeric inputs,
- client-ID validation,
- creation of new assessment histories,
- append behavior for existing clients,
- isolation of assessment histories between different clients.

Tests use temporary directories for persistence testing so the test suite does not modify the application's normal assessment-data file.

Run the complete test suite with:

~~~bash
python3 -m unittest discover -s tests -p "test_*.py"
~~~

---

## Running the Application

The project was developed and tested using Python 3.12.

No third-party Python packages are currently required for the command-line application.

Run:

~~~bash
python3 main.py
~~~

The application will request:

~~~text
Client ID
Age
Gender
Weight
Height
Resting heart rate
Physical Activity Level
Three skinfold measurements
Weight lifted
Repetitions completed
~~~

It then calculates the available assessment metrics, displays the results, and appends the assessment to the selected client's JSON history.

---

## Example Workflow

~~~text
Enter client ID: client_001
Enter age: 30
Enter gender: male
Enter weight: 180
Enter height: 70
Enter resting heart rate: 60
Enter PAL: 1.75

Enter skinfold measurements:
Chest: 10
Abdominal: 20
Thigh: 30

Enter weight lifted: 200
Enter repetitions completed: 8
~~~

Example calculated outputs include:

~~~text
Estimated RMR
Estimated TDEE
Body-fat percentage
Estimated VO₂max
Heart-rate zones
Estimated 1RM
Training-intensity ranges
~~~

The complete input and result set is then stored as a timestamped assessment.

---

## References and Equation Traceability

Published equations, implementation choices, and known limitations are documented in:

~~~text
docs/references.md
~~~

The reference document distinguishes between:

~~~text
Published equation
        ↓
Toolkit implementation
        ↓
Implementation restriction / design decision
        ↓
Known limitations
~~~

This distinction is intentional.

For example:

- the Tanaka HRmax equation comes from published research,
- the 1–10 repetition restriction for 1RM estimation is a toolkit design choice,
- the five-zone heart-rate model is treated as a toolkit convention,
- the current training-intensity percentage ranges remain provisional behavior.

See:

[Fitness Assessment Toolkit References](docs/references.md)

---

## Related Project

### Fuzzy Workout Intensity Recommender

The Fitness Assessment Toolkit is related to a separate project:

[Fuzzy Workout Intensity Recommender](https://github.com/maxlouissaint/Fuzzy-Workout-Intensity-Recommender)

The projects intentionally address different responsibilities.

### Responsibility Split

#### Fitness Assessment Toolkit

~~~text
Question:
"What is the person's estimated fitness state?"

Examples:
RMR
TDEE
Body composition
Heart-rate information
Estimated VO₂max
Estimated 1RM
Assessment history
~~~

#### Fuzzy Workout Intensity Recommender

~~~text
Question:
"Given recovery indicators, how intense should today's workout be?"

Inputs include:
Sleep
Change in resting heart rate
HRV
Soreness
Motivation
~~~

The fuzzy project uses a Mamdani fuzzy inference system to produce a recovery-informed workout-intensity recommendation.

---

## Planned Integration Interface

The two projects currently remain independent.

A future extension may define a shared data interface between them:

~~~text
Fitness Assessment Toolkit
        │
        │ assessment / fitness state
        ▼
Defined Data Interface
        │
        ▼
Fuzzy Workout Intensity Recommender
        │
        │ recovery-based intensity recommendation
        ▼
Training Guidance
~~~

The intended design is to preserve separation of responsibilities rather than combine both applications into one codebase.

A possible future data-level workflow is:

~~~text
Historical Fitness Assessment
        │
        ├── resting heart-rate history
        ├── strength estimates
        ├── body-composition history
        └── other assessment context
                    │
                    ▼
            Recovery Inputs
                    │
                    ▼
          Fuzzy Inference Model
                    │
                    ▼
       Workout-Intensity Recommendation
~~~

An executable integration has **not yet been implemented**, and this repository does not currently claim that the training-intensity ranges are generated by the fuzzy model.

Future integration work would require a defined and validated interface contract between the two projects.

---

## Future Development

Potential future extensions include:

- defining the data contract between the Fitness Assessment Toolkit and the Fuzzy Workout Intensity Recommender,
- evaluating how historical resting-heart-rate data could support recovery assessment,
- separating persistence logic behind a more formal storage interface,
- improving CLI input handling and user feedback,
- evaluating alternative or additional assessment methods,
- validating any integration between fitness metrics and training recommendations before presenting it as supported behavior.

These are future directions rather than current project capabilities.

---

## Design Considerations

Several design choices were intentionally made during refactoring.

### Preserve Raw Inputs

Each historical assessment stores both:

~~~text
inputs
results
~~~

This allows previous assessments to retain the measurements that produced the calculated values.

It also provides a foundation for recalculating historical assessments if an estimation method changes in a later version.

### Separate Calculation and Persistence Responsibilities

Calculation modules are responsible for fitness calculations.

`DataManipulation.py` is responsible for storing and retrieving assessment data.

This avoids embedding JSON storage behavior directly inside the calculation functions.

### Avoid Personally Identifying Client Data

The persistence model uses caller-defined identifiers such as:

~~~text
client_001
~~~

rather than requiring names or contact information.

### Fail Explicitly on Invalid Inputs

Calculation functions validate assumptions before executing rather than silently accepting unsupported values.

Examples include:

~~~text
Unsupported gender
Unsupported age
Non-positive skinfold measurements
Invalid resting heart rate
Unsupported PAL
Invalid repetition count
Invalid client identifier
~~~

### Preserve Historical Assessments

Saving a new assessment for an existing client appends the record rather than replacing previous records.

This supports longitudinal assessment history.

---

## Scope and Limitations

The project demonstrates software implementation of fitness-estimation methods.

It does **not** represent:

- a clinically validated fitness-assessment platform,
- a medical device,
- diagnostic software,
- direct laboratory measurement,
- individualized medical guidance,
- individualized nutrition guidance,
- individualized exercise prescription.

Estimation accuracy depends on the limitations of the underlying equations and the quality of the input measurements.

Examples include:

- age-predicted HRmax may differ significantly from measured HRmax,
- skinfold estimates depend heavily on measurement technique,
- estimated VO₂max is not equivalent to laboratory gas-exchange testing,
- estimated 1RM may differ from directly tested maximum strength,
- PAL-based TDEE depends on the selected activity level.

See `docs/references.md` for equation-specific limitations.

---

## Development Status

Current implementation status:

~~~text
Core calculation refactor       Complete
Input validation                Complete
Unit conversion cleanup         Complete
Published equation review       Complete
Automated unit testing          Complete
Assessment-history persistence  Complete
Reference documentation         Complete
README / portfolio polish       Complete
Fuzzy-model integration         Planned
~~~

The current codebase is intended to serve as a stable baseline before additional integration work is introduced.

---

## Repository Focus

This repository focuses on the **fitness-assessment and historical-data side** of the larger concept.

The related fuzzy-inference project remains separate so each repository maintains a clear engineering responsibility:

~~~text
Assessment
    ↓
Fitness Assessment Toolkit

Decision Support
    ↓
Fuzzy Workout Intensity Recommender

Future Integration
    ↓
Defined interface between the two systems
~~~

This separation allows both projects to evolve independently while leaving a clear path toward a larger integrated fitness decision-support system.
