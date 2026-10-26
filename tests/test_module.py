import unittest
from src.database import DatabaseTriangle
from src.calculate import CalculateTriangle


class TestDatabaseModule(unittest.TestCase):
    def setUp(self):
        self.db = DatabaseTriangle("triangle.db")

    def tearDown(self):
        self.db.close()

    def test_db_add_and_get(self):
        self.db.add(6.0, 4.0, 5.0, "разносторонний", "")
        result = self.db.get(6.0, 4.0, 5.0)
        self.assertIsNotNone(result)
        self.assertEqual(result["type"], "разносторонний")
        self.assertEqual(result["exception"], "")

    def test_db_delete(self):
        self.db.add(1.0, 2.0, 3.0, "не треугольник", "Ошибка")
        is_deleted = self.db.delete(1.0, 2.0, 3.0)
        self.assertTrue(is_deleted)
        result = self.db.get(1.0, 2.0, 3.0)
        self.assertIsNone(result)


class TestCalculateModule(unittest.TestCase):
    def setUp(self):
        self.calc = CalculateTriangle()

    def test_process_valid_float_strings(self):
        tri_type, vertices, message = self.calc.process("1.5", "1.5", "1.5")
        self.assertEqual(tri_type, "равносторонний")
        self.assertEqual(len(vertices), 3)

    def test_process_zero_side(self):
        tri_type, vertices, message = self.calc.process("0", "5", "5")
        self.assertEqual(tri_type, "не треугольник")
        self.assertEqual(vertices, [(-1, -1), (-1, -1), (-1, -1)])