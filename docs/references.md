# Fitness Assessment Toolkit — References

This document records the published sources, implementation choices, and important limitations behind the estimation methods used in the **Fitness Assessment Toolkit**.

The toolkit is intended for educational and software-engineering purposes. Its calculations are estimates derived from published equations and are **not substitutes for direct laboratory measurement, medical evaluation, diagnosis, or individualized professional guidance**.

---

## 1. Resting Metabolic Rate (RMR)

### Implemented Method

The toolkit uses the revised Harris–Benedict equations reported by Roza and Shizgal (1984).

For men:

~~~text
RMR = 88.362
    + (13.397 × weight_kg)
    + (4.799 × height_cm)
    - (5.677 × age_years)
~~~

For women:

~~~text
RMR = 447.593
    + (9.247 × weight_kg)
    + (3.098 × height_cm)
    - (4.330 × age_years)
~~~

Output is expressed in **kcal/day**.

### Implementation Notes

The toolkit accepts weight in pounds and height in inches at the command line, converts them to kilograms and centimeters, and then applies the equations above.

### Limitations

These are predictive equations for resting energy expenditure, not direct calorimetry.

Roza and Shizgal reported that the Harris–Benedict equations estimated resting energy expenditure in normally nourished individuals with limited precision and were unreliable in malnourished patients. Individual estimates may therefore differ materially from measured resting energy expenditure.

### Primary Reference

Roza, A. M., & Shizgal, H. M. (1984). The Harris Benedict equation reevaluated: resting energy requirements and the body cell mass. *The American Journal of Clinical Nutrition, 40*(1), 168–182.

DOI: https://doi.org/10.1093/ajcn/40.1.168
PubMed: https://pubmed.ncbi.nlm.nih.gov/6741850/

---

## 2. Total Daily Energy Expenditure (TDEE) and Physical Activity Level (PAL)

### Implemented Method

The toolkit estimates total daily energy expenditure as:

~~~text
TDEE = RMR × PAL
~~~

The toolkit currently accepts PAL values from **1.40 to 2.40**.

Command-line guidance is grouped as:

| PAL Range | Toolkit Label |
|---|---|
| 1.40–1.69 | Sedentary / light activity |
| 1.70–1.99 | Active / moderate activity |
| 2.00–2.40 | Vigorous activity |

### Implementation Notes

Physical Activity Level is commonly expressed as total energy expenditure relative to basal or resting energy expenditure.

The toolkit applies the selected PAL value to its **estimated RMR**:

~~~text
Estimated TDEE = Estimated RMR × PAL
~~~

The 1.40–2.40 interval is the range supported by this implementation and should not be interpreted as a universal physiological limit.

### Limitations

PAL represents habitual activity rather than an exact measurement of an individual's energy expenditure on a particular day.

The final TDEE estimate combines uncertainty from:

- the RMR prediction equation,
- the selected PAL value,
- normal day-to-day variation in activity and energy expenditure.

### References

Food and Agriculture Organization of the United Nations, World Health Organization, & United Nations University. (2004). *Human Energy Requirements: Report of a Joint FAO/WHO/UNU Expert Consultation*. FAO Food and Nutrition Technical Report Series 1.

https://www.fao.org/4/y5686e/y5686e00.htm

National Cancer Institute, Division of Cancer Control and Population Sciences. *Physical Activity Level (PAL)*.

https://cancercontrol.cancer.gov/brp/research/group-evaluated-measures/adopt/pal

Johansson, G., & Westerterp, K. R. (2008). Assessment of the physical activity level with two questions: validation with doubly labeled water. *International Journal of Obesity, 32*, 1031–1033.

DOI: https://doi.org/10.1038/ijo.2008.42
PubMed: https://pubmed.ncbi.nlm.nih.gov/18392036/

---

## 3. Body-Fat Percentage from Skinfold Measurements

### Implemented Method

The toolkit uses the Jackson–Pollock generalized three-site body-density equations followed by a body-density-to-body-fat conversion using the Siri equation.

### Men

Supported age range in the implementation:

~~~text
18–61 years
~~~

Skinfold sites:

~~~text
Chest
Abdominal
Thigh
~~~

Let:

~~~text
S = sum of the three skinfold measurements in millimeters
~~~

Body density is estimated as:

~~~text
Db = 1.10938
   - (0.0008267 × S)
   + (0.0000016 × S²)
   - (0.0002574 × age)
~~~

### Women

Supported age range in the implementation:

~~~text
18–55 years
~~~

Skinfold sites:

~~~text
Triceps
Suprailiac
Thigh
~~~

Body density is estimated as:

~~~text
Db = 1.0994921
   - (0.0009929 × S)
   + (0.0000023 × S²)
   - (0.0001392 × age)
~~~

### Siri Conversion

The estimated body density is converted to estimated body-fat percentage using:

~~~text
Body Fat % = ((4.95 / Db) - 4.50) × 100
~~~

### Implementation Notes

The toolkit validates:

- supported sex-specific age ranges,
- numeric skinfold measurements,
- finite skinfold measurements,
- skinfold measurements greater than zero.

### Limitations

Skinfold-based body-fat estimation is sensitive to:

- measurement technique,
- anatomical site identification,
- caliper accuracy,
- tester consistency,
- population differences.

The Jackson–Pollock equations estimate **body density**, not body-fat percentage directly. The subsequent Siri conversion introduces an additional model assumption when translating body density into estimated body-fat percentage.

The men's generalized equations were developed using adult men ranging from 18 to 61 years of age.

The women's generalized equations were developed using women ranging from 18 to 55 years of age. The original study also cautioned that care should be exercised when applying the equations to women over age 40.

### Primary References

Jackson, A. S., & Pollock, M. L. (1978). Generalized equations for predicting body density of men. *British Journal of Nutrition, 40*(3), 497–504.

DOI: https://doi.org/10.1079/BJN19780152
PubMed: https://pubmed.ncbi.nlm.nih.gov/718832/

Jackson, A. S., Pollock, M. L., & Ward, A. (1980). Generalized equations for predicting body density of women. *Medicine & Science in Sports & Exercise, 12*(3), 175–181.

DOI: https://doi.org/10.1249/00005768-198023000-00009
PubMed: https://pubmed.ncbi.nlm.nih.gov/7402053/

Siri, W. E. (1961). Body composition from fluid spaces and density: analysis of methods. In J. Brozek & A. Henschel (Eds.), *Techniques for Measuring Body Composition*. National Academy of Sciences–National Research Council.

### Accessible Equation Reference

University of New Mexico — Len Kravitz, *Body Composition Assessment*.

https://www.unm.edu/~lkravitz/Article%20folder/bodycomp.html

This source reproduces the Jackson–Pollock three-site equations and the Siri conversion used by the toolkit.

---

## 4. Age-Predicted Maximum Heart Rate

### Implemented Method

The toolkit uses the Tanaka, Monahan, and Seals equation:

~~~text
Estimated HRmax = 208 - (0.7 × age)
~~~

Output is expressed in:

~~~text
beats per minute (bpm)
~~~

### Implementation Notes

The equation is used when a directly measured maximum heart rate is unavailable.

The implementation currently requires an adult age of at least 18 years.

### Limitations

Age-based HRmax equations describe population-level trends and can have substantial error for an individual.

The result should therefore be interpreted as an **estimated maximum heart rate**, not as an individual's measured physiological maximum.

### Primary Reference

Tanaka, H., Monahan, K. D., & Seals, D. R. (2001). Age-predicted maximal heart rate revisited. *Journal of the American College of Cardiology, 37*(1), 153–156.

DOI: https://doi.org/10.1016/S0735-1097(00)01054-8
PubMed: https://pubmed.ncbi.nlm.nih.gov/11153730/

---

## 5. Estimated VO₂max from Heart-Rate Ratio

### Implemented Method

The toolkit estimates mass-specific VO₂max using the ratio between maximum heart rate and resting heart rate.

For men:

~~~text
Estimated VO₂max = 15.3 × (HRmax / HRrest)
~~~

For women:

~~~text
Estimated VO₂max = 14.5 × (HRmax / HRrest)
~~~

Output is expressed in:

~~~text
mL·kg⁻¹·min⁻¹
~~~

### Implementation Notes

The toolkit first estimates HRmax using the Tanaka equation and then applies the heart-rate-ratio method.

Therefore, the implemented calculation is effectively:

~~~text
age
  ↓
Tanaka estimated HRmax
  ↓
HRmax / resting HR
  ↓
heart-rate-ratio VO₂max estimate
~~~

### Limitations

This is an **indirect estimate**, not a direct VO₂max measurement.

The original heart-rate-ratio study evaluated well-trained men and reported lower estimation error when measured HRmax was used than when age-predicted HRmax was substituted.

The authors noted that applicability to other populations required additional validation.

A follow-up study in trained women reported different proportionality factors for men and women:

~~~text
Men:   15.3
Women: 14.5
~~~

These values should not be interpreted as universally validated constants across all ages, fitness levels, or populations.

Because this toolkit combines an **age-predicted HRmax** with the heart-rate-ratio method, uncertainty from both estimation methods contributes to the final VO₂max estimate.

### Primary References

Uth, N., Sørensen, H., Overgaard, K., & Pedersen, P. K. (2004). Estimation of VO₂max from the ratio between HRmax and HRrest—the Heart Rate Ratio Method. *European Journal of Applied Physiology, 91*(1), 111–115.

DOI: https://doi.org/10.1007/s00421-003-0988-y
PubMed: https://pubmed.ncbi.nlm.nih.gov/14624296/

Uth, N. (2005). Gender difference in the proportionality factor between the mass specific VO₂max and the ratio between HRmax and HRrest. *International Journal of Sports Medicine, 26*(9), 763–767.

DOI: https://doi.org/10.1055/s-2005-837443
PubMed: https://pubmed.ncbi.nlm.nih.gov/16237622/

---

## 6. Heart-Rate Training Zones

### Implemented Method

The toolkit currently divides estimated maximum heart rate into five continuous percentage bands:

~~~text
Zone 1: 50–60% HRmax
Zone 2: 60–70% HRmax
Zone 3: 70–80% HRmax
Zone 4: 80–90% HRmax
Zone 5: 90–100% HRmax
~~~

### Status

This five-zone model is currently treated as a **toolkit implementation convention**.

It is not intended to represent an individualized physiological threshold model.

### Limitations

Training zones can be defined using several different approaches, including:

- measured maximum heart rate,
- heart-rate reserve,
- ventilatory thresholds,
- lactate thresholds,
- sport-specific physiological testing.

The toolkit's zones should therefore be interpreted as simple percentage-based reference bands derived from estimated HRmax.

---

## 7. Estimated One-Repetition Maximum (1RM)

### Implemented Method

The toolkit uses the Epley equation for sets containing more than one repetition:

~~~text
Estimated 1RM = weight_lifted × (1 + repetitions / 30)
~~~

For a true single repetition:

~~~text
repetitions = 1

Estimated 1RM = weight_lifted
~~~

The implementation accepts:

~~~text
1–10 repetitions
~~~

### Implementation Notes

Returning the observed weight for a one-repetition set avoids estimating a value that has already been directly observed.

The 1–10 repetition restriction is a **toolkit design choice** intended to avoid extending the prediction equation too far into higher-repetition muscular-endurance work.

That restriction is separate from the mathematical form of the Epley equation itself.

### Limitations

Estimated 1RM equations do not replace direct 1RM testing.

Prediction accuracy can vary based on:

- exercise,
- training status,
- repetition range,
- fatigue,
- technique,
- individual strength-endurance characteristics.

Prediction uncertainty generally becomes more important as the number of repetitions increases.

### Reference

Epley, B. (1985). *Boyd Epley Workout*. Lincoln, Nebraska: Body Enterprises.

The commonly reproduced Epley form is:

~~~text
1RM = weight × (1 + reps / 30)
~~~

---

## 8. Training-Intensity Ranges

The current application also displays percentage-based training-intensity ranges for categories including:

~~~text
Endurance
Hypertrophy
Strength
Power
~~~

These ranges remain part of the current application behavior.

However, the project does **not currently claim that the specific percentage boundaries have been independently validated within this repository**.

They should therefore be treated as provisional training-guidance behavior rather than as one of the literature-backed estimation methods documented above.

### Potential Future Integration

A future extension may connect this functionality to the separate:

**Fuzzy Workout Intensity Recommender**

That project evaluates workout-intensity recommendations using recovery-related inputs such as:

~~~text
Sleep
Change in resting heart rate
Heart-rate variability
Soreness
Motivation
~~~

The intended architectural relationship would remain separated by responsibility:

~~~text
Fitness Assessment Toolkit
        │
        │ fitness and assessment state
        ▼
Defined integration interface
        │
        ▼
Fuzzy Workout Intensity Recommender
        │
        │ readiness-based intensity recommendation
        ▼
Training guidance
~~~

No executable integration between the two projects is currently claimed.

---

## 9. Assessment Persistence and Data Structure

The toolkit stores assessment histories in JSON using anonymous caller-supplied client identifiers rather than names or other identifying profile information.

The high-level persistence structure is:

~~~text
data
└── clients
    └── client_id
        └── assessments
            ├── assessment
            ├── assessment
            └── ...
~~~

Each assessment contains:

~~~text
timestamp
inputs
results
~~~

Example conceptual structure:

~~~text
client_001
└── assessments
    ├── assessment 1
    │   ├── timestamp
    │   ├── inputs
    │   └── results
    │
    └── assessment 2
        ├── timestamp
        ├── inputs
        └── results
~~~

New assessments are appended to a client's existing history rather than replacing previous assessments.

The JSON hierarchy, anonymous client identifier, timestamp format, and append-only history behavior are **software-design decisions** and do not originate from the physiological references in this document.

---

## 10. Interpretation and Scope

The Fitness Assessment Toolkit demonstrates the implementation, validation, persistence, and unit testing of published fitness-estimation equations in a modular Python application.

The references in this document support the **origin and intended context of the implemented equations**, but they do not imply that:

- every estimate is accurate for every individual,
- the software has undergone clinical validation,
- the software is a medical device,
- estimated values are equivalent to laboratory measurements,
- the application provides medical diagnosis,
- the application provides individualized nutrition prescriptions,
- the application provides individualized exercise prescriptions.

Where the toolkit introduces its own restrictions, conventions, or software-design decisions, those decisions are identified separately from the published equations.

---

## Related Project

### Fuzzy Workout Intensity Recommender

The **Fuzzy Workout Intensity Recommender** is maintained as a separate project because it addresses a different problem:

~~~text
Fitness Assessment Toolkit
"What is the person's estimated fitness state?"

Fuzzy Workout Intensity Recommender
"Given recovery indicators, how intense should today's workout be?"
~~~

A future integration may define a shared data interface between the projects while preserving their independent responsibilities and repositories.

Until such an interface is implemented and validated, the two repositories should be presented as **related but independent projects**.
