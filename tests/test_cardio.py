import unittest

from CardioFitnessAssessment import (
    calculate_heart_rate_zones,
    estimate_max_heart_rate,
    estimate_vo2_max,
)


class TestMaximumHeartRate(unittest.TestCase):
    def test_tanaka_reference_values(self):
        cases = (
            (18, 195.4),
            (30, 187.0),
            (40, 180.0),
            (60, 166.0),
        )

        for age, expected in cases:
            with self.subTest(age=age):
                self.assertAlmostEqual(
                    estimate_max_heart_rate(age),
                    expected,
                    places=9,
                )

    def test_age_below_adult_range_raises_value_error(self):
        for age in (17, 0, -1):
            with self.subTest(age=age):
                with self.assertRaises(ValueError):
                    estimate_max_heart_rate(age)

    def test_nonnumeric_age_raises_value_error(self):
        with self.assertRaises(ValueError):
            estimate_max_heart_rate("30")

    def test_boolean_age_raises_value_error(self):
        with self.assertRaises(ValueError):
            estimate_max_heart_rate(True)

    def test_age_producing_invalid_hrmax_raises_value_error(self):
        with self.assertRaises(ValueError):
            estimate_max_heart_rate(300)


class TestVo2Estimation(unittest.TestCase):
    def test_male_reference_case(self):
        result = estimate_vo2_max(
            190,
            60,
            "male",
        )

        self.assertAlmostEqual(
            result,
            48.45,
            places=9,
        )

    def test_female_reference_case(self):
        result = estimate_vo2_max(
            190,
            60,
            "female",
        )

        self.assertAlmostEqual(
            result,
            45.916666666666664,
            places=9,
        )

    def test_gender_is_case_insensitive(self):
        lower = estimate_vo2_max(
            190,
            60,
            "male",
        )

        upper = estimate_vo2_max(
            190,
            60,
            "MALE",
        )

        self.assertAlmostEqual(lower, upper, places=12)

    def test_invalid_heart_rates_raise_value_error(self):
        cases = (
            (0, 60, "male"),
            (190, 0, "male"),
            (60, 60, "male"),
            (50, 60, "male"),
        )

        for case in cases:
            with self.subTest(case=case):
                with self.assertRaises(ValueError):
                    estimate_vo2_max(*case)

    def test_invalid_gender_raises_value_error(self):
        with self.assertRaises(ValueError):
            estimate_vo2_max(
                190,
                60,
                "other",
            )


class TestHeartRateZones(unittest.TestCase):
    def test_five_zone_ranges(self):
        zones = calculate_heart_rate_zones(190)

        expected = {
            "Zone 1": (95.0, 114.0),
            "Zone 2": (114.0, 133.0),
            "Zone 3": (133.0, 152.0),
            "Zone 4": (152.0, 171.0),
            "Zone 5": (171.0, 190.0),
        }

        self.assertEqual(set(zones), set(expected))

        for zone, expected_range in expected.items():
            with self.subTest(zone=zone):
                actual_min, actual_max = zones[zone]
                expected_min, expected_max = expected_range

                self.assertAlmostEqual(
                    actual_min,
                    expected_min,
                    places=9,
                )

                self.assertAlmostEqual(
                    actual_max,
                    expected_max,
                    places=9,
                )

    def test_zone_boundaries_are_continuous(self):
        zones = calculate_heart_rate_zones(187)

        names = list(zones)

        for index in range(len(names) - 1):
            current_max = zones[names[index]][1]
            next_min = zones[names[index + 1]][0]

            self.assertAlmostEqual(
                current_max,
                next_min,
                places=12,
            )

    def test_nonpositive_max_hr_raises_value_error(self):
        for max_hr in (0, -1):
            with self.subTest(max_hr=max_hr):
                with self.assertRaises(ValueError):
                    calculate_heart_rate_zones(max_hr)


if __name__ == "__main__":
    unittest.main()
