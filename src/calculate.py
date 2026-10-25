import math


class CalculateTriangle:
    def identify_type(self, a: float, b: float, c: float):
        if (math.isclose(a + b, c) or math.isclose(b + c, a) or
                math.isclose(a + c, b) or a + b < c or b + c < a or a + c < b):
            return 'не треугольник'
        if math.isclose(a, b) and math.isclose(b, c):
            return 'равносторонний'
        if math.isclose(a, b) or math.isclose(b, c) or math.isclose(c, a):
            return 'равнобедренный'
        return 'разносторонний'

    def calculate_vertices_by_angles(self, a, b, c):
        cos_beta = (a * a + c * c - b * b) / (2 * a * c)
        beta = math.acos(max(-1.0, min(1.0, cos_beta)))

        x1, y1 = 0.0, 0.0
        x2, y2 = a, 0.0

        x3 = c * math.cos(beta)
        y3 = c * math.sin(beta)


        min_x, max_x = min(x1, x2, x3), max(x1, x2, x3)
        min_y, max_y = min(y1, y2, y3), max(y1, y2, y3)
        width, height = max_x - min_x, max_y - min_y
        scale = 100.0 / max(width, height, 1e-9)

        def scale_point(x, y):
            return (int(round((x - min_x) * scale)),
                    int(round((y - min_y) * scale)))

        return [scale_point(x1, y1),
                scale_point(x2, y2),
                scale_point(x3, y3)]

    def process(self, string1: str, string2: str, string3: str):
        try:
            a = float(string1)
            b = float(string2)
            c = float(string3)
        except (ValueError, TypeError):
            return "", [(-2, -2), (-2, -2), (-2, -2)], "Нечисловые данные"

        if a <= 0 or b <= 0 or c <= 0:
            return "не треугольник", [(-1, -1), (-1, -1), (-1, -1)], "Стороны должны быть положительными"

        tri_type = self.identify_type(a, b, c)

        if tri_type == "не треугольник":
            return tri_type, [(-1, -1), (-1, -1), (-1, -1)], "Условие треугольника не выполнено"

        vertices = self.calculate_vertices_by_angles(a, b, c)
        return tri_type, vertices, ""