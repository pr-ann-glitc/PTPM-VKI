from email import message

from src.calculate import CalculateTriangle
from src.database import DatabaseTriangle
from src.user_interface import AbstractUserInterface
from src.external_service import AbstractExternalService

class TriangleController:
    def __init__(self,
                 calculator: CalculateTriangle,
                 database: DatabaseTriangle,
                 console: AbstractUserInterface,
                 external: AbstractExternalService):
        self.calculator = calculator
        self.database = database
        self.console = console
        self.external = external

    def process(self, message: str = ""):
        s1 = self.console.get_input("Сторона 1: ")
        s2 = self.console.get_input("Сторона 2: ")
        s3 = self.console.get_input("Сторона 3: ")

        try:
            a, b, c = float(s1), float(s2), float(s3)
        except (ValueError, TypeError):
            result = {
                "type": "",
                "vertices": [],
                "error": "Нечисловые данные",
            }
            self.console.show_result(f"Ошибка: {result['error']}")
            self.external.send(f"Ошибка: {result['error']}")
            return result
        cached = self.database.get(a, b, c)
        if cached:
            result = {
                "type": cached["type"],
                "vertices": [],
                "error": cached["exception"] or "",
            }
            message = "Такая запись уже есть в БД"
        else:
            tri_type, vertices, error = self.calculator.process(s1, s2, s3)
            self.database.add(a, b, c, tri_type, error)
            result = {
                "type": tri_type,
                "vertices": vertices,
                "error": error,
            }
        message = f"Тип: {result['type']}; Ошибка: {result['error']}"
        self.external.send(message)

        self.console.show_result(message)
        return result