class Converter:
    @staticmethod
    def do(x: float) -> int:
        match x:
            case x if x >= 100.7:
                return 1000
            case x if 0 < x < 100.7:
                return int(x)
            case x if x == 0:
                raise ValueError("Введен 0")
            case x if -30.4 <= x < 0:
                return int(x) - 5
            case x if x <= -30.5:
                return -2000
