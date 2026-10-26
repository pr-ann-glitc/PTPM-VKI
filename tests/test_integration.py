import unittest
from src.controller import TriangleController
from src.database import DatabaseTriangle
from src.user_interface import AbstractUserInterface
from src.external_service import AbstractExternalService
from src.calculate import CalculateTriangle


class ImitationUserInput(AbstractUserInterface):
    def __init__(self, inputs):
        self._inputs = list(inputs)
        self.shown = []
    def get_input(self, prompt):
        return self._inputs.pop(0)
    def show_result(self, message):
        self.shown.append(message)

class ImitationService(AbstractExternalService):
    def __init__(self):
        self.sent = []

    def send(self, message):
        self.sent.append(message)
        return True


class TestTriangleCalculation(unittest.TestCase):
    def test_full_to_db(self):
        db = DatabaseTriangle("triangle.db")
        console = ImitationUserInput(["3", "4", "5"])
        external = ImitationService()
        controller = TriangleController(CalculateTriangle(), db, console, external)

        result = controller.process()

        self.assertEqual(result["type"], "разносторонний")
        self.assertIsNotNone(db.get(3.0, 4.0, 5.0))
        self.assertEqual(len(external.sent), 1)
        db.close()

    def test_no_triangle(self):
        db = DatabaseTriangle("triangle.db")
        console = ImitationUserInput(["1", "4", "5"])
        external = ImitationService()
        controller = TriangleController(CalculateTriangle(), db, console, external)

        result = controller.process()

        self.assertEqual(result["type"], "не треугольник")
        self.assertEqual(result["error"], "Условие треугольника не выполнено")

        db.close()

    def test_second_call_uses_db_cache(self):
        db = DatabaseTriangle("triangle.db")
        external = ImitationService()

        console1 = ImitationUserInput(["5", "5", "5"])
        controller1 = TriangleController(CalculateTriangle(), db, console1, external)
        result1 = controller1.process()

        self.assertEqual(result1["type"], "равносторонний")

        console2 = ImitationUserInput(["5", "5", "5"])
        controller2 = TriangleController(CalculateTriangle(), db, console2, external)
        result2 = controller2.process()

        self.assertEqual(result2["type"], "равносторонний")
        self.assertEqual(len(external.sent), 2)
        db.close()
