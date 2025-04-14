class Singleton(type):
    _instances = None

    def __new__(cls):
        if cls._instances is None:
            cls._instances = super().__new__(cls)
        return cls._instances
