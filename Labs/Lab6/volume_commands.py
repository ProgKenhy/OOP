from command import Command


class VolumeUpCommand(Command):
    """Команда увеличения громкости"""

    def __init__(self, volume_step=10):
        self.volume_step = volume_step
        self.current_volume = 50

    def execute(self):
        """Увеличивает громкость"""
        old_volume = self.current_volume
        self.current_volume = min(100, self.current_volume + self.volume_step)
        return f"volume increased +{self.volume_step}%"

    def undo(self):
        """Уменьшает громкость обратно"""
        self.current_volume = max(0, self.current_volume - self.volume_step)
        return f"volume decreased -{self.volume_step}%"

    def get_description(self):
        return f"Volume Up (+{self.volume_step}%)"


class VolumeDownCommand(Command):
    """Команда уменьшения громкости"""

    def __init__(self, volume_step=10):
        self.volume_step = volume_step
        self.current_volume = 50

    def execute(self):
        """Уменьшает громкость"""
        old_volume = self.current_volume
        self.current_volume = max(0, self.current_volume - self.volume_step)
        return f"volume decreased -{self.volume_step}%"

    def undo(self):
        """Увеличивает громкость обратно"""
        self.current_volume = min(100, self.current_volume + self.volume_step)
        return f"volume increased +{self.volume_step}%"

    def get_description(self):
        return f"Volume Down (-{self.volume_step}%)"
