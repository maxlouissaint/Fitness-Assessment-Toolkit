import unittest

from StrengthAndEnduranceAssessment import estimate_one_rep_max


class TestOneRepMaxEstimation(unittest.TestCase):
    def test_single_rep_returns_observed_weight(self):
        self.assertEqual(
            estimate_one_rep_max(200, 1),
            200.0,
        )

    def test_eight_rep_reference_case(self):
        self.assertAlmostEqual(
            estimate_one_rep_max(200, 8),
            253.33333333333331,
            places=9,
        )

    def test_ten_rep_reference_case(self):
        self.assertAlmostEqual(
            estimate_one_rep_max(100, 10),
            133.33333333333331,
            places=9,
        )

    def test_nonpositive_weight_raises_value_error(self):
        for weight in (0, -100):
            with self.subTest(weight=weight):
                with self.assertRaises(ValueError):
                    estimate_one_rep_max(weight, 5)

    def test_repetitions_below_range_raise_value_error(self):
        for reps in (0, -1):
            with self.subTest(reps=reps):
                with self.assertRaises(ValueError):
                    estimate_one_rep_max(100, reps)

    def test_repetitions_above_range_raise_value_error(self):
        with self.assertRaises(ValueError):
            estimate_one_rep_max(100, 11)

    def test_fractional_repetitions_raise_value_error(self):
        with self.assertRaises(ValueError):
            estimate_one_rep_max(100, 5.5)

    def test_boolean_repetitions_raise_value_error(self):
        with self.assertRaises(ValueError):
            estimate_one_rep_max(100, True)


if __name__ == "__main__":
    unittest.main()
