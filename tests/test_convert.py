import unittest
from src.converter import Converter


class TestConverter(unittest.TestCase):
    def test_far_above_100_7(self):
        self.assertEqual(Converter.do(7982.4), 1000)

    def test_exactly_100_7(self):
        self.assertEqual(Converter.do(100.7), 1000)

    def test_slightly_above_100_7(self):
        self.assertEqual(Converter.do(100.8), 1000)

    def test_between_0_and_100_7(self):
        self.assertEqual(Converter.do(45.5), 45)

    def test_slightly_below_100_7(self):
        self.assertEqual(Converter.do(100.6), 100)

    def test_small_positive(self):
        self.assertEqual(Converter.do(0.5), 0)

    def test_one_point_zero(self):
        self.assertEqual(Converter.do(1.0), 1)

    def test_is_0(self):
        with self.assertRaises(ValueError):
            Converter.do(0)

    def test_between_30_4_and_0(self):
        self.assertEqual(Converter.do(-28.8), -33)

    def test_negative_zero_point_five(self):
        self.assertEqual(Converter.do(-0.5), -5)

    def test_exactly_minus_30_4(self):
        self.assertEqual(Converter.do(-30.4), -30 - 5)

    def test_close_to_zero_negative(self):
        self.assertEqual(Converter.do(-0.1), -5)

    def test_less_30_5(self):
        self.assertEqual(Converter.do(-90.6), -2000)

    def test_exactly_minus_30_5(self):
        self.assertEqual(Converter.do(-30.5), -2000)

    def test_slightly_below_minus_30_5(self):
        self.assertEqual(Converter.do(-30.6), -2000)