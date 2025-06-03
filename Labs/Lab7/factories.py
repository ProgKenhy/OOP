from implementations import DebugLogger, ReleaseLogger


def create_console_logger():
    return DebugLogger("[CONSOLE]")


def create_file_logger():
    return ReleaseLogger("FILE")
