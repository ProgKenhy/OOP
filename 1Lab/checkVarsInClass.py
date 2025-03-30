from typing import ClassVar

from pydantic import BaseModel, Field, ConfigDict


class Point2d(BaseModel):
    WIDTH: ClassVar[int] = 1080
    HEIGHT: ClassVar[int] = 540
    x: int = Field(..., ge=0, le=WIDTH)
    y: int = Field(..., ge=0, le=HEIGHT)
    model_config = ConfigDict(validate_assignment=True)


class Vector2d:
    __slots__ = ("__x", "__y")

    def __init__(self, x: int, y: int):
        self.__x = x
        self.__y = y

    # region Свойства x и y с валидацией типа
    @property
    def x(self) -> int:
        return self.__x

    @x.setter
    def x(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("x must be an integer")
        self.__x = value

    @property
    def y(self) -> int:
        return self.__y

    @y.setter
    def y(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("y must be an integer")
        self.__y = value

    # endregion

    # region Альтернативные конструкторы
    @classmethod
    def from_points(cls, start: 'Point2d', end: 'Point2d') -> 'Vector2d':
        return cls(end.x - start.x, end.y - start.y)

    # endregion

    # region Индексация и итерация
    def __getitem__(self, index: int) -> int:
        if index == 0: return self.x
        if index == 1: return self.y
        raise IndexError("Index out of range (0-1)")

    def __setitem__(self, index: int, value: int) -> None:
        if index == 0:
            self.x = value
        elif index == 1:
            self.y = value
        else:
            raise IndexError("Index out of range (0-1)")

    def __iter__(self) -> iter:
        yield self.x
        yield self.y

    def __len__(self) -> int:
        return 2

    # endregion

    # region Сравнение
    def __eq__(self, other: object) -> bool:
        return isinstance(other, Vector2d) and self.x == other.x and self.y == other.y

    # endregion

    # region Строковое представление
    def __str__(self) -> str:
        return f"Vector2d({self.x}, {self.y})"

    def __repr__(self) -> str:
        return f"Vector2d(x={self.x}, y={self.y})"

    # endregion

    # region Векторные операции
    def __abs__(self) -> float:
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def __add__(self, other: 'Vector2d') -> 'Vector2d':
        if not isinstance(other, Vector2d):
            raise TypeError("Can only add Vector2d to Vector2d")
        return Vector2d(self.x + other.x, self.y + other.y)

    def __sub__(self, other: 'Vector2d') -> 'Vector2d':
        if not isinstance(other, Vector2d):
            raise TypeError("Can only subtract Vector2d from Vector2d")
        return Vector2d(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: (int, float)) -> 'Vector2d':
        if not isinstance(scalar, (int, float)):
            raise TypeError("Scalar must be numeric")
        x = self.x * scalar
        y = self.y * scalar
        if x != int(x) or y != int(y):
            raise ValueError("Non-integer components after multiplication")
        return Vector2d(int(x), int(y))

    def __rmul__(self, scalar: (int, float)) -> 'Vector2d':
        return self.__mul__(scalar)

    def __truediv__(self, scalar: (int, float)) -> 'Vector2d':
        if not isinstance(scalar, (int, float)):
            raise TypeError("Scalar must be numeric")
        if scalar == 0:
            raise ZeroDivisionError("Division by zero")
        x = self.x / scalar
        y = self.y / scalar
        if not (x.is_integer() and y.is_integer()):
            raise ValueError("Non-integer components after division")
        return Vector2d(int(x), int(y))

    # endregion

    # region Произведения
    def dot(self, other: 'Vector2d') -> int:
        """Скалярное произведение (метод экземпляра)"""
        return self.x * other.x + self.y * other.y

    @staticmethod
    def dot_product(v1: 'Vector2d', v2: 'Vector2d') -> int:
        """Скалярное произведение (статический метод)"""
        return v1.x * v2.x + v1.y * v2.y

    def cross(self, other: 'Vector2d') -> int:
        """Векторное произведение (псевдоскаляр для 2D)"""
        return self.x * other.y - self.y * other.x

    @staticmethod
    def cross_product(v1: 'Vector2d', v2: 'Vector2d') -> int:
        """Векторное произведение (статический метод)"""
        return v1.x * v2.y - v1.y * v2.x

    @staticmethod
    def triple_product(v1: 'Vector2d', v2: 'Vector2d', v3: 'Vector2d') -> int:
        """Смешанное произведение для 2D (расширение до 3D)"""
        return (v1.x * (v2.y * v3.x - v2.x * v3.y) -
                v1.y * (v2.x * v3.x - v2.x * v3.x) +
                (v1.x * v2.y - v1.y * v2.x) * v3.y)
    # endregion


if __name__ == "__main__":
    first = Point2d(x=960, y=400)
    second = Point2d(x=560, y=450)
    print(first == second)

    try:
        obj = Point2d(x=-10, y=-21)
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

    print(repr(first))

    v1 = Vector2d(3, 4)
    v2 = Vector2d.from_points(second, first)

    print(v1 + v2)
    print(v1.dot(v2))
    print(Vector2d.cross_product(v1, v2))
    print(abs(v1))
    print(v1 * 2)
