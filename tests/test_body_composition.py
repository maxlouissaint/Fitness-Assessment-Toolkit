import math
import unittest

from BodyCompositionAssessment import (
    calculate_body_fat_skinfold,
    estimate_rmr,
    estimate_tdee,
)


class TestBodyFatEstimation(unittest.TestCase):
    def test_male_reference_case(self):
        result = calculate_body_fat_skinfold(
            "male",
            30,
            10,
            20,
            30,
        )

        self.assertAlmostEqual(
            result,
            17.94527592700428,
            places=6,
        )

    def test_female_reference_case(self):
        result = calculate_body_fat_skinfold(
            "female",
            30,
            12,
            18,
            22,
        )

        self.assertAlmostEqual(
            result,
            21.471452879761888,
            places=6,
        )

    def test_gender_is_case_insensitive(self):
        lower = calculate_body_fat_skinfold(
            "male",
            30,
            10,
            20,
            30,
        )

        mixed = calculate_body_fat_skinfold(
            "MALE",
            30,
            10,
            20,
            30,
        )

        self.assertAlmostEqual(lower, mixed, places=12)

    def test_male_age_boundaries_are_accepted(self):
        calculate_body_fat_skinfold("male", 18, 10, 20, 30)
        calculate_body_fat_skinfold("male", 61, 10, 20, 30)

    def test_female_age_boundaries_are_accepted(self):
        calculate_body_fat_skinfold("female", 18, 12, 18, 22)
        calculate_body_fat_skinfold("female", 55, 12, 18, 22)

    def test_invalid_gender_raises_value_error(self):
        with self.assertRaises(ValueError):
            calculate_body_fat_skinfold(
                "other",
                30,
                10,
                20,
                30,
            )

    def test_male_age_outside_study_range_raises_value_error(self):
        for age in (17, 62):
            with self.subTest(age=age):
                with self.assertRaises(ValueError):
                    calculate_body_fat_skinfold(
                        "male",
                        age,
                        10,
                        20,
                        30,
                    )

    def test_female_age_outside_study_range_raises_value_error(self):
        for age in (17, 56):
            with self.subTest(age=age):
                with self.assertRaises(ValueError):
                    calculate_body_fat_skinfold(
                        "female",
                        age,
                        12,
                        18,
                        22,
                    )

    def test_invalid_skinfold_values_raise_value_error(self):
        invalid_values = (0, -1, math.nan, math.inf)

        for value in invalid_values:
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    calculate_body_fat_skinfold(
                        "male",
                        30,
                        value,
                        20,
                        30,
                    )


class TestRmrEstimation(unittest.TestCase):
    def test_male_reference_case(self):
        result = estimate_rmr(
            "male",
            180,
            70,
            30,
        )

        self.assertAlmostEqual(
            result,
            1865.1452804681123,
            places=9,
        )

    def test_female_reference_case(self):
        result = estimate_rmr(
            "female",
            150,
            65,
            30,
        )

        self.assertAlmostEqual(
            result,
            1458.3345526989024,
            places=9,
        )

    def test_invalid_gender_raises_value_error(self):
        with self.assertRaises(ValueError):
            estimate_rmr(
                "other",
                180,
                70,
                30,
            )

    def test_nonpositive_rmr_inputs_raise_value_error(self):
        cases = (
            ("male", 0, 70, 30),
            ("male", -180, 70, 30),
            ("male", 180, 0, 30),
            ("male", 180, -70, 30),
            ("male", 180, 70, 0),
            ("male", 180, 70, -1),
        )

        for case in cases:
            with self.subTest(case=case):
                with self.assertRaises(ValueError):
                    estimate_rmr(*case)

    def test_nonfinite_rmr_inputs_raise_value_error(self):
        cases = (
            ("male", math.nan, 70, 30),
            ("male", 180, math.inf, 30),
            ("male", 180, 70, math.nan),
        )

        for case in cases:
            with self.subTest(case=case):
                with self.assertRaises(ValueError):
                    estimate_rmr(*case)

    def test_nonnumeric_rmr_input_raises_value_error(self):
        with self.assertRaises(ValueError):
            estimate_rmr(
                "male",
                180,
                70,
                "30",
            )


class TestTdeeEstimation(unittest.TestCase):
    def test_reference_case(self):
        result = estimate_tdee(
            1865.1452804681123,
            1.75,
        )

        self.assertAlmostEqual(
            result,
            3264.0042408191963,
            places=9,
        )

    def test_supported_pal_boundaries(self):
        cases = (
            (1.40, 2520.0),
            (1.69, 3042.0),
            (1.70, 3060.0),
            (1.99, 3582.0),
            (2.00, 3600.0),
            (2.40, 4320.0),
        )

        for pal, expected in cases:
            with self.subTest(pal=pal):
                self.assertAlmostEqual(
                    estimate_tdee(1800, pal),
                    expected,
                    places=9,
                )

    def test_invalid_rmr_raises_value_error(self):
        for rmr in (0, -1800, math.nan, math.inf):
            with self.subTest(rmr=rmr):
                with self.assertRaises(ValueError):
                    estimate_tdee(rmr, 1.75)

    def test_pal_outside_supported_range_raises_value_error(self):
        for pal in (1.39, 2.41):
            with self.subTest(pal=pal):
                with self.assertRaises(ValueError):
                    estimate_tdee(1800, pal)

    def test_nonfinite_pal_raises_value_error(self):
        for pal in (math.nan, math.inf):
            with self.subTest(pal=pal):
                with self.assertRaises(ValueError):
                    estimate_tdee(1800, pal)

    def test_nonnumeric_pal_raises_value_error(self):
        with self.assertRaises(ValueError):
            estimate_tdee(
                1800,
                "1.75",
            )


if __name__ == "__main__":
    unittest.main()
