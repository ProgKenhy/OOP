"""
Point2d:
- x: int
- y: int

"""
from dataclasses import dataclass


@dataclass
class Point2d:
    x: int
    y: int
    SCREEN_WIDTH = 1080
    SCREEN_HEIGHT = 720

    @property
    def x_y(self, x: int, y: int):
        if not isinstance(x, int) or not isinstance(y, int):
            raise TypeError('x and y must be integers')
        if not (0 <= x <= self.SCREEN_WIDTH and 0 <= y <= self.SCREEN_HEIGHT):
            raise ValueError('x, y must be between 0 and SCREEN_WIDTH')
        else:
            self.x = x
            self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __repr__(self):
        return f"Point({self.x}, {self.y})"

if __name__ == "__main__":
    first = Point2d(960, 400)
    second = Point2d(1200, 2000)

    try:
        obj = Point2d(-10, 1)
    except ValueError as e:
        print(f"Ошибка: {e}")

    print(first)
    print(second)


