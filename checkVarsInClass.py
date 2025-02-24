from dataclasses import dataclass, field


@dataclass
class Point2d:
    SCREEN_WIDTH: int = field(default=1080, init=False, repr=False)
    SCREEN_HEIGHT: int = field(default=540, init=False, repr=False)

    _x: int = field(init=False, repr=False)
    _y: int = field(init=False, repr=False)

    def __init__(self, x: int, y: int):
        self.x = x  # используем сеттер для x
        self.y = y  # используем сеттер для y

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value: int):
        if not isinstance(value, int):
            raise TypeError('x must be integer')
        if not (0 <= value <= self.SCREEN_WIDTH):
            raise ValueError('x must be between 0 and SCREEN_WIDTH')
        else:
            self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value: int):
        if not isinstance(value, int):
            raise TypeError('y must be integer')
        if not (0 <= value <= self.SCREEN_HEIGHT):
            raise ValueError('y must be between 0 and SCREEN_HEIGHT')
        else:
            self._y = value

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __repr__(self):
        return f"Point({self.x}, {self.y})"


if __name__ == "__main__":
    first = Point2d(960, 400)
    print(first)

    try:
        obj = Point2d(-10, 1)
    except ValueError as e:
        print(f"Ошибка: {e}")

    try:
        first.x = 2000
    except ValueError as e:
        print(f"Ошибка: {e}")

    try:
        first.y = 1000
    except ValueError as e:
        print(f"Ошибка: {e}")

    print(first)
