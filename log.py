import logging
import sys
import math

log_format = "%(asctime)s | [%(levelname)-7s] | %(message)s"
date_format = "%Y-%m-%d %H:%M:%S"

logging.basicConfig(
    level=logging.DEBUG,
    format=log_format,
    datefmt=date_format,
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("logs/file_txt.log", encoding="utf-8")
    ]
)

logging.info("Логгер успешно сконфигурирован")
logging.info("Приложение запущено")


def identify_type(a: float, b:float, c:float):
    if a + b <= c or b + c <= a or c + a <= b:
        return 'не треугольник'
    if a == b == c:
        return 'равносторонний'
    if a == b or b == c or c == a:
        return 'равнобедренный'
    return 'разносторонний'

def calculate_vertices_by_angles(a, b, c):
    cos_beta = (a*a + c*c - b*b) / (2*a*c)
    beta = math.acos(max(-1.0, min(1.0, cos_beta)))

    x1, y1 = 0.0, 0.0
    x2, y2 = a, 0.0

    x3 = c * math.cos(beta)
    y3 = c * math.sin(beta)

    logging.debug(f"Угол beta = {math.degrees(beta):.2f}")

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

def process(string1: str, string2: str, string3: str):
    params = {"A": string1, "B": string2, "C": string3}
    try:
        a = float(string1)
        b = float(string2)
        c = float(string3)
    except (ValueError, TypeError):
        logging.error(f"Параметры = {params}\n"
                      f"Причина: нечисловые данные")
        return "", [(-2, -2), (-2, -2), (-2, -2)]

    if a <= 0 or b <= 0 or c <= 0:
        logging.error(f"Параметры = {params}\n"
                      f"Причина: стороны должны быть положительными")
        return "не треугольник", [(-1, -1), (-1, -1), (-1, -1)]

    tri_type = identify_type(a, b, c)
    logging.debug(f"Тип треугольника: {tri_type}")

    if tri_type == "не треугольник":
        logging.warning(f"Запрос обработан | параметры = {params}\n"
                        f"Результат: не треугольник")
        return tri_type, [(-1, -1), (-1, -1), (-1, -1)]

    vertices = calculate_vertices_by_angles(a, b, c)
    logging.info(f"Успешно | параметры = {params}\n"
                 f"Тип = {tri_type}, вершины = {vertices}")
    return tri_type, vertices

def main():
    try:
        string1 = input('Сторона 1: ')
        string2 = input('Сторона 2: ')
        string3 = input('Сторона 3: ')
        process(string1, string2, string3)

    except Exception:
        logging.exception("Критическая ошибка при выполнении программы")
        raise

if __name__ == "__main__":
    main()