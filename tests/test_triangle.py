import unittest
from src.triangle import identify_type, process, calculate_vertices_by_angles


class TestIdentifyType(unittest.TestCase):
    def test_scalene_triangle(self):
        self.assertEqual(identify_type(3, 4, 5), "разносторонний")

    def test_isosceles_triangle_two_equal_sides(self):
        self.assertEqual(identify_type(5, 5, 8), "равнобедренный")

    def test_equilateral_triangle(self):
        self.assertEqual(identify_type(5, 5, 5), "равносторонний")

    def test_not_triangle(self):
        self.assertEqual(identify_type(2, 3, 10), "не треугольник")

    def test_not_triangle_sum_equals(self):
        self.assertEqual(identify_type(3, 4, 7), "не треугольник")

    def test_not_triangle_onepointzero(self):
        self.assertEqual(identify_type(0.1, 0.2, 0.3), "не треугольник")


class TestProcessInput(unittest.TestCase):
    def test_non_numeric_first_arg(self):
        self.assertEqual(process("abc", "4", "5"),
                         ("", [(-2, -2), (-2, -2), (-2, -2)]))

    def test_non_numeric_second_arg(self):
        self.assertEqual(process("3", "xyz", "5"),
                         ("", [(-2, -2), (-2, -2), (-2, -2)]))

    def test_non_numeric_third_arg(self):
        self.assertEqual(process("3", "4", "!!!"),
                         ("", [(-2, -2), (-2, -2), (-2, -2)]))

    def test_negative_side_returns_not_triangle(self):
        result, vertices = process("-3", "4", "5")
        self.assertEqual(result, "не треугольник")
        self.assertEqual(vertices, [(-1, -1), (-1, -1), (-1, -1)])

    def test_zero_side_returns_not_triangle(self):
        result, vertices = process("0", "4", "5")
        self.assertEqual(result, "не треугольник")

    def test_valid_scalene_triangle(self):
        result, vertices = process("3", "4", "5")
        self.assertEqual(result, "разносторонний")
        self.assertEqual(len(vertices), 3)

    def test_valid_equilateral_triangle(self):
        result, _ = process("5", "5", "5")
        self.assertEqual(result, "равносторонний")

    def test_valid_isosceles_triangle(self):
        result, _ = process("5", "5", "8")
        self.assertEqual(result, "равнобедренный")

    def test_not_triangle_valid_numbers(self):
        result, _ = process("1", "2", "10")
        self.assertEqual(result, "не треугольник")


class TestCalculateVertices(unittest.TestCase):
    def test_returns_three_vertices(self):
        vertices = calculate_vertices_by_angles(3, 4, 5)
        self.assertEqual(len(vertices), 3)

    def test_vertices_within_0_100_range(self):
        vertices = calculate_vertices_by_angles(3, 4, 5)
        for x, y in vertices:
            self.assertGreaterEqual(x, 0)
            self.assertLessEqual(x, 100)
            self.assertGreaterEqual(y, 0)
            self.assertLessEqual(y, 100)

    def test_equilateral_triangle_symmetry(self):
        vertices = calculate_vertices_by_angles(5, 5, 5)
        self.assertEqual(len(vertices), 3)
