from command import Command


class MediaPlayerCommand(Command):
    """Команда управления медиаплеером"""

    def __init__(self):
        self.is_playing = False

    def execute(self):
        """Запускает/останавливает медиаплеер"""
        if not self.is_playing:
            self.is_playing = True
            return "media player launched"
        else:
            self.is_playing = False
            return "media player stopped"

    def undo(self):
        """Возвращает предыдущее состояние медиаплеера"""
        if self.is_playing:
            self.is_playing = False
            return "media player closed"
        else:
            self.is_playing = True
            return "media player launched"

    def get_description(self):
        return "Toggle Media Player"


class ClearScreenCommand(Command):
    """Дополнительная команда очистки экрана"""

    def __init__(self, output_manager):
        self.output_manager = output_manager
        self.backup_text = ""

    def execute(self):
        """Очищает экран"""
        self.backup_text = self.output_manager.get_text()
        self.output_manager.clear()
        return "screen cleared"

    def undo(self):
        """Восстанавливает текст"""
        self.output_manager.restore_text(self.backup_text)
        return "screen restored"

    def get_description(self):
        return "Clear Screen"
