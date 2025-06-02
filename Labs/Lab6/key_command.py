from command import Command


class KeyCommand(Command):
    """Команда для печати символа"""

    def __init__(self, char, output_manager):
        self.char = char
        self.output_manager = output_manager

    def execute(self):
        """Печатает символ"""
        self.output_manager.add_text(self.char)
        return f"{self.char}"

    def undo(self):
        """Стирает последний символ"""
        if self.output_manager.can_backspace():
            removed_char = self.output_manager.backspace()
            return f"undo"
        return "undo"

    def get_description(self):
        return f"Print '{self.char}'"
