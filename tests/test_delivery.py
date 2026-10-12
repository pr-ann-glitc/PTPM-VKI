import unittest
from src.Delivery import calculate_delivery_cost


class TestWeightValidation(unittest.TestCase):
    def test_weight_below_minimum(self):
        self.assertEqual(calculate_delivery_cost(0.05, 100, "обычный"), (-1, "0000-00-00"))

    def test_weight_exactly_minimum(self):
        cost, date = calculate_delivery_cost(0.1, 100, "обычный")
        self.assertNotEqual(cost, -1)

    def test_weight_above_maximum(self):
        self.assertEqual(calculate_delivery_cost(50.1, 100, "обычный"), (-1, "0000-00-00"))

    def test_weight_exactly_maximum(self):
        cost, date = calculate_delivery_cost(50.0, 100, "обычный")
        self.assertNotEqual(cost, -1)

    def test_negative_weight(self):
        self.assertEqual(calculate_delivery_cost(-5, 100, "обычный"), (-1, "0000-00-00"))


class TestDistanceValidation(unittest.TestCase):
    def test_distance_zero(self):
        self.assertEqual(calculate_delivery_cost(10, 0, "обычный"), (-1, "0000-00-00"))

    def test_distance_negative(self):
        self.assertEqual(calculate_delivery_cost(10, -50, "обычный"), (-1, "0000-00-00"))

    def test_distance_exactly_one(self):
        cost, date = calculate_delivery_cost(10, 1, "обычный")
        self.assertNotEqual(cost, -1)

    def test_distance_exactly_5000(self):
        cost, date = calculate_delivery_cost(10, 5000, "обычный")
        self.assertNotEqual(cost, -1)

    def test_distance_above_5000(self):
        self.assertEqual(calculate_delivery_cost(10, 5001, "обычный"), (-1, "0000-00-00"))


class TestPackageTypeValidation(unittest.TestCase):
    def test_normal_type_is_valid(self):
        cost, _ = calculate_delivery_cost(10, 100, "обычный")
        self.assertNotEqual(cost, -1)

    def test_fragile_type_is_valid(self):
        cost, _ = calculate_delivery_cost(10, 100, "хрупкий")
        self.assertNotEqual(cost, -1)

    def test_dangerous_type_is_valid(self):
        cost, _ = calculate_delivery_cost(10, 100, "опасный")
        self.assertNotEqual(cost, -1)

    def test_unknown_type_returns_error(self):
        self.assertEqual(calculate_delivery_cost(10, 100, "опасны"), (-1, "0000-00-00"))

    def test_empty_type(self):
        self.assertEqual(calculate_delivery_cost(10, 100, ""), (-1, "0000-00-00"))


class TestCostCalculation(unittest.TestCase):
    def test_base_cost_for_light_normal_package(self):
        # 200 + 100*5 = 700
        cost, _ = calculate_delivery_cost(3, 100, "обычный")
        self.assertEqual(cost, 700)

    def test_medium_weight_multiplier_1_2(self):
        # (200 + 100*5) * 1.2 = 840
        cost, _ = calculate_delivery_cost(10, 100, "обычный")
        self.assertEqual(cost, 840)

    def test_heavy_weight_multiplier_1_5(self):
        # (200 + 100*5) * 1.5 = 1050
        cost, _ = calculate_delivery_cost(25, 100, "обычный")
        self.assertEqual(cost, 1050)

    def test_weight_boundary_5kg_no_multiplier(self):
        # 5 кг → без коэффициента
        cost, _ = calculate_delivery_cost(5.0, 100, "обычный")
        self.assertEqual(cost, 700)

    def test_fragile_surcharge_300(self):
        # 700 + 300 = 1000
        cost, _ = calculate_delivery_cost(3, 100, "хрупкий")
        self.assertEqual(cost, 1000)

    def test_dangerous_surcharge_1000(self):
        # 700 + 1000 = 1700
        cost, _ = calculate_delivery_cost(3, 100, "опасный")
        self.assertEqual(cost, 1700)


class TestExpressDelivery(unittest.TestCase):
    def test_express_increases_cost(self):
        normal_cost, _ = calculate_delivery_cost(10, 100, "обычный", is_express=False)
        express_cost, _ = calculate_delivery_cost(10, 100, "обычный", is_express=True)
        self.assertGreater(express_cost, normal_cost)

    def test_express_reduces_delivery_time(self):
        _, normal_date = calculate_delivery_cost(10, 1000, "обычный", is_express=False)
        _, express_date = calculate_delivery_cost(10, 1000, "обычный", is_express=True)
        self.assertLess(express_date, normal_date)

    def test_express_minimum_one_day(self):
        _, express_date = calculate_delivery_cost(10, 100, "обычный", is_express=True)
        self.assertGreaterEqual(express_date, "2026-09-03")


class TestDeliveryDate(unittest.TestCase):
    def test_short_distance_takes_one_day(self):
        _, date = calculate_delivery_cost(10, 100, "обычный")
        self.assertEqual(date, "2026-09-03")

    def test_medium_distance_days(self):
        _, date = calculate_delivery_cost(10, 1000, "обычный")
        self.assertEqual(date, "2026-09-05")

    def test_long_distance_days(self):
        _, date = calculate_delivery_cost(10, 5000, "обычный")
        self.assertEqual(date, "2026-09-13")

    def test_distance_499_takes_one_day(self):
        _, date = calculate_delivery_cost(10, 499, "обычный")
        self.assertEqual(date, "2026-09-04")