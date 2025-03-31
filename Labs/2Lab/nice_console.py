import sys
from enum import Enum
from typing import Tuple
import shutil
import os


class Color(Enum):
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    YELLOW = (255, 255, 0)
    CYAN = (0, 255, 255)
    MAGENTA = (255, 0, 255)


class Printer:
    _font = None
    font_height = 5

    @classmethod
    def get_terminal_size(cls):
        try:
            return shutil.get_terminal_size()
        except:
            # Возвращаем объект с размерами по умолчанию
            class TerminalSize:
                def __init__(self, columns, lines):
                    self.columns = columns
                    self.lines = lines

            return TerminalSize(80, 24)

    @classmethod
    def full_clear(cls):
        size = cls.get_terminal_size()

        # Для Windows
        if os.name == 'nt':
            os.system('')
        # Для Unix-систем
        else:
            # Очистка экрана + буфера прокрутки + курсор в начало
            print("\033[2J", end="")

        # Дополнительные пустые строки на случай частичной очистки
        print("\n" * size.lines, end="")
        print("\033[H", end="")  # Возврат курсора в начало

    @classmethod
    def load_font(cls, filename: str = "font.txt") -> None:
        cls._font = {}
        try:
            with open(filename, "r") as f:
                content = f.read().split("\n\n")

            for block in content:
                if not block.strip():
                    continue
                lines = block.split("\n")
                char = lines[0].strip()
                if not char:
                    continue

                template = []
                for line in lines[1:]:
                    if line.strip():
                        template.append(line.rstrip())

                if len(template) < cls.font_height:
                    template.extend([''] * (cls.font_height - len(template)))
                elif len(template) > cls.font_height:
                    template = template[:cls.font_height]

                cls._font[char] = template

            if ' ' not in cls._font:
                cls._font[' '] = [' '] * cls.font_height

        except FileNotFoundError:
            print(f"Font file '{filename}' not found.", file=sys.stderr)
            raise

    @classmethod
    def print_static(cls, text: str, color: Color, position: Tuple[int, int], symbol: str) -> None:
        if cls._font is None:
            cls.load_font()

        size = cls.get_terminal_size()
        x, y = position

        # Корректируем позицию, если выходит за границы
        if y < 1:
            y = 1
        if y + cls.font_height > size.lines:
            y = max(1, size.lines - cls.font_height - 1)

        current_x = x

        for char in text.upper():
            if char not in cls._font:
                char = ' '

            char_lines = cls._font[char]
            replaced = [line.replace('*', symbol) for line in char_lines]
            char_width = max(len(line) for line in replaced) if replaced else 1

            # Перенос на новую строку если не помещается
            if current_x + char_width > size.columns:
                current_x = x
                y += cls.font_height + 1
            if y + cls.font_height > size.lines:
                y = 2
                print("\033[2J", end="")

            # Выводим символ
            for i, line in enumerate(replaced):
                print(
                    f"\033[{y + i};{current_x}H\033[38;2;{color.value[0]};{color.value[1]};{color.value[2]}m{line}\033[0m",
                    end="")

            current_x += char_width + 2

        print(f"\033[{y + cls.font_height + 1};0H")  # Переводим курсор

    def __init__(self, color: Color, position: Tuple[int, int], symbol: str):
        self.color = color
        self.position = position
        self.symbol = symbol
        self.current_y = position[1]
        if Printer._font is None:
            Printer.load_font()

    def __enter__(self):
        print("\033[s", end="")  # Сохраняем позицию курсора
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("\033[u\033[0m", end="")  # Восстанавливаем позицию и сбрасываем стиль

    def print(self, text: str) -> None:
        if Printer._font is None:
            Printer.load_font()

        size = Printer.get_terminal_size()
        x, y = self.position[0], self.current_y

        if y + Printer.font_height > size.lines:
            y = size.lines

        current_x = x

        for char in text.upper():
            if char not in Printer._font:
                char = ' '

            char_lines = Printer._font[char]
            replaced = [line.replace('*', self.symbol) for line in char_lines]
            char_width = max(len(line) for line in replaced) if replaced else 1

            # Перенос строки при необходимости
            if current_x + char_width > size.columns:
                current_x = x
                y += Printer.font_height + 1
            if y + Printer.font_height > size.lines:
                y = 2
                print("\033[2J", end="")

            # Вывод символа
            for i, line in enumerate(replaced):
                print(
                    f"\033[{y + i};{current_x}H\033[38;2;{self.color.value[0]};{self.color.value[1]};{self.color.value[2]}m{line}\033[0m",
                    end="")

            current_x += char_width + 2

        self.current_y = y + Printer.font_height + 1
        print(f"\033[{self.current_y};0H")


if __name__ == "__main__":
    # Активация поддержки ANSI в Windows
    if os.name == 'nt':
        os.system('')

    Printer.full_clear()
    current_y = 1

    try:
        Printer.load_font()

        Printer.print_static("HELLO MY BEAUTIFUL WORLD AND another", Color.RED, (5, current_y), "#")
        current_y += (Printer.font_height+1) * 3

        with Printer(Color.GREEN, (2, current_y), "@") as printer:
            printer.print("IT'S")
            current_y += Printer.font_height + 1
            printer.print("PYTHON PROGRAMMING LANGUAGE IS AWESOME")
            current_y += (Printer.font_height+1) * 2

        with Printer(Color.BLUE, (10, current_y), "*") as printer:
            printer.print("COOL TEXT! " * 5)
            current_y += (Printer.font_height+1) * 2

        with Printer(Color.YELLOW, (5, current_y), "*") as printer:
            printer.print("12345")
            current_y += Printer.font_height

    except Exception as e:
        print(f"\033[{current_y};1HError: {e}\033[0m", file=sys.stderr)
        current_y += 1

    input(f"\033[{current_y};1HPress Enter to exit...")
