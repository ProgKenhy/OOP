class OutputManager:
    """Управляет выводом текста в консоль и файл"""

    def __init__(self, filename="output.txt"):
        self.text = ""
        self.filename = filename
        self.console_log = []

    def add_text(self, char):
        """Добавляет символ к тексту"""
        self.text += char
        self._log_to_console_and_file(char)

    def backspace(self):
        """Удаляет последний символ"""
        if self.text:
            removed_char = self.text[-1]
            self.text = self.text[:-1]
            return removed_char
        return ""

    def can_backspace(self):
        """Проверяет, можно ли удалить символ"""
        return len(self.text) > 0

    def get_text(self):
        """Возвращает текущий текст"""
        return self.text

    def clear(self):
        """Очищает текст"""
        self.text = ""

    def restore_text(self, text):
        """Восстанавливает текст"""
        self.text = text

    def _log_to_console_and_file(self, message):
        """Записывает сообщение в консоль и файл"""
        # Вывод в консоль
        print(message, end='', flush=True)

        # Запись в файл
        try:
            with open(self.filename, 'a', encoding='utf-8') as f:
                f.write(message)
        except Exception as e:
            print(f"\nError writing to file: {e}")

    def log_command(self, message):
        """Логирует выполнение команды"""
        print(message)
        try:
            with open(self.filename, 'a', encoding='utf-8') as f:
                f.write(f"{message}\n")
        except Exception as e:
            print(f"Error writing to file: {e}")

    def log_current_state(self):
        """Логирует текущее состояние текста"""
        if self.text:
            print(f"\nCurrent text: {self.text}")
            try:
                with open(self.filename, 'a', encoding='utf-8') as f:
                    f.write(f" {self.text}\n")
            except Exception as e:
                print(f"Error writing to file: {e}")
        else:
            print("\nCurrent text: (empty)")
            try:
                with open(self.filename, 'a', encoding='utf-8') as f:
                    f.write(" (empty)\n")
            except Exception as e:
                print(f"Error writing to file: {e}")

    def clear_file(self):
        """Очищает файл вывода"""
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                f.write("")
        except Exception as e:
            print(f"Error clearing file: {e}")
