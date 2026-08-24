import unittest

from Utils import (
    inches_to_centimeters,
    kilograms_to_pounds,
    pounds_to_kilograms,
)


class TestUnitConversions(unittest.TestCase):
    def test_pounds_to_kilograms(self):
        self.assertAlmostEqual(
            pounds_to_kilograms(180),
            81.64746439263358,
            places=9,
        )

    def test_kilograms_to_pounds(self):
        self.assertAlmostEqual(
            kilograms_to_pounds(81.6466),
            179.99809436,
            places=8,
        )

    def test_inches_to_centimeters(self):
        self.assertAlmostEqual(
            inches_to_centimeters(70),
            177.8,
            places=9,
        )

    def test_zero_values(self):
        self.assertEqual(pounds_to_kilograms(0), 0)
        self.assertEqual(kilograms_to_pounds(0), 0)
        self.assertEqual(inches_to_centimeters(0), 0)

    def test_non_numeric_conversion_input_raises_type_error(self):
        with self.assertRaises(TypeError):
            pounds_to_kilograms("180")

        with self.assertRaises(TypeError):
            kilograms_to_pounds("80")

        with self.assertRaises(TypeError):
            inches_to_centimeters("70")


if __name__ == "__main__":
    unittest.main()
