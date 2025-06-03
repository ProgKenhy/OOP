from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, Any, Type, Callable, Optional, List
import inspect
import threading


class LifeStyle(Enum):
    """Жизненные циклы объектов"""
    PER_REQUEST = "per_request"
    SCOPED = "scoped"
    SINGLETON = "singleton"


class DIContainer:
    """Контейнер для управления зависимостями"""

    def __init__(self):
        self._registrations: Dict[Type, Dict] = {}
        self._singletons: Dict[Type, Any] = {}
        self._scoped_instances: Dict[Type, Any] = {}
        self._scope_active = False
        self._lock = threading.Lock()

    def register(self, interface_type: Type, implementation_type: Type = None,
                 lifestyle: LifeStyle = LifeStyle.PER_REQUEST,
                 factory_method: Callable = None, **params):
        """
        Регистрация зависимости

        Args:
            interface_type: Тип интерфейса
            implementation_type: Тип реализации (если не указан factory_method)
            lifestyle: Жизненный цикл объекта
            factory_method: Фабричный метод для создания объекта
            **params: Дополнительные параметры для конструктора
        """
        if factory_method and implementation_type:
            raise ValueError("Нельзя указывать одновременно implementation_type и factory_method")

        if not factory_method and not implementation_type:
            raise ValueError("Должен быть указан либо implementation_type, либо factory_method")

        self._registrations[interface_type] = {
            'implementation_type': implementation_type,
            'factory_method': factory_method,
            'lifestyle': lifestyle,
            'params': params
        }

    def get_instance(self, interface_type: Type):
        """
        Получение экземпляра по интерфейсу

        Args:
            interface_type: Тип интерфейса

        Returns:
            Экземпляр класса, реализующего интерфейс
        """
        if interface_type not in self._registrations:
            raise ValueError(f"Интерфейс {interface_type.__name__} не зарегистрирован")

        registration = self._registrations[interface_type]
        lifestyle = registration['lifestyle']

        # Singleton - всегда один экземпляр
        if lifestyle == LifeStyle.SINGLETON:
            return self._get_singleton(interface_type, registration)

        # Scoped - один экземпляр в пределах scope
        elif lifestyle == LifeStyle.SCOPED:
            return self._get_scoped(interface_type, registration)

        # PerRequest - новый экземпляр каждый раз
        else:
            return self._create_instance(registration)

    def _get_singleton(self, interface_type: Type, registration: Dict):
        """Получение singleton экземпляра"""
        with self._lock:
            if interface_type not in self._singletons:
                self._singletons[interface_type] = self._create_instance(registration)
            return self._singletons[interface_type]

    def _get_scoped(self, interface_type: Type, registration: Dict):
        """Получение scoped экземпляра"""
        if not self._scope_active:
            raise ValueError("Scoped экземпляр может быть получен только внутри scope")

        if interface_type not in self._scoped_instances:
            self._scoped_instances[interface_type] = self._create_instance(registration)
        return self._scoped_instances[interface_type]

    def _create_instance(self, registration: Dict):
        """Создание нового экземпляра"""
        if registration['factory_method']:
            return registration['factory_method']()

        implementation_type = registration['implementation_type']
        params = registration['params']

        # Получаем параметры конструктора
        constructor_signature = inspect.signature(implementation_type.__init__)
        constructor_params = {}

        # Автоматическое внедрение зависимостей
        for param_name, param in constructor_signature.parameters.items():
            if param_name == 'self':
                continue

            # Если параметр явно передан
            if param_name in params:
                constructor_params[param_name] = params[param_name]
            # Если параметр - зарегистрированный интерфейс
            elif param.annotation in self._registrations:
                constructor_params[param_name] = self.get_instance(param.annotation)
            # Если параметр имеет значение по умолчанию
            elif param.default is not inspect.Parameter.empty:
                constructor_params[param_name] = param.default

        return implementation_type(**constructor_params)

    def create_scope(self):
        """Создание нового scope для scoped объектов"""
        return DIScope(self)


class DIScope:
    """Контекстный менеджер для scoped объектов"""

    def __init__(self, container: DIContainer):
        self.container = container

    def __enter__(self):
        self.container._scope_active = True
        self.container._scoped_instances = {}
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.container._scope_active = False
        self.container._scoped_instances = {}


# ========================= ИНТЕРФЕЙСЫ =========================

class ILogger(ABC):
    """Интерфейс для логирования"""

    @abstractmethod
    def log(self, message: str) -> None:
        pass


class IDataService(ABC):
    """Интерфейс для работы с данными"""

    @abstractmethod
    def get_data(self) -> List[str]:
        pass

    @abstractmethod
    def save_data(self, data: str) -> bool:
        pass


class INotificationService(ABC):
    """Интерфейс для уведомлений"""

    @abstractmethod
    def send_notification(self, recipient: str, message: str) -> bool:
        pass


# ========================= РЕАЛИЗАЦИИ =========================

# Logger implementations
class DebugLogger(ILogger):
    def __init__(self, prefix: str = "[DEBUG]"):
        self.prefix = prefix
        print(f"Создан DebugLogger с префиксом: {prefix}")

    def log(self, message: str) -> None:
        print(f"{self.prefix} {message}")


class ReleaseLogger(ILogger):
    def __init__(self, log_level: str = "INFO"):
        self.log_level = log_level
        print(f"Создан ReleaseLogger с уровнем: {log_level}")

    def log(self, message: str) -> None:
        print(f"[{self.log_level}] {message}")


# DataService implementations
class DebugDataService(IDataService):
    def __init__(self, logger: ILogger, connection_string: str = "debug_db"):
        self.logger = logger
        self.connection_string = connection_string
        self.data = ["debug_item1", "debug_item2"]
        self.logger.log(f"DebugDataService инициализирован с БД: {connection_string}")

    def get_data(self) -> List[str]:
        self.logger.log("Получение данных из debug базы")
        return self.data.copy()

    def save_data(self, data: str) -> bool:
        self.logger.log(f"Сохранение в debug базу: {data}")
        self.data.append(data)
        return True


class ReleaseDataService(IDataService):
    def __init__(self, logger: ILogger, connection_string: str = "prod_db"):
        self.logger = logger
        self.connection_string = connection_string
        self.data = ["prod_item1", "prod_item2", "prod_item3"]
        self.logger.log(f"ReleaseDataService инициализирован с БД: {connection_string}")

    def get_data(self) -> List[str]:
        self.logger.log("Получение данных из производственной базы")
        return self.data.copy()

    def save_data(self, data: str) -> bool:
        self.logger.log(f"Сохранение в производственную базу: {data}")
        self.data.append(data)
        return True


# NotificationService implementations
class DebugNotificationService(INotificationService):
    def __init__(self, logger: ILogger, data_service: IDataService):
        self.logger = logger
        self.data_service = data_service
        self.logger.log("DebugNotificationService инициализирован")

    def send_notification(self, recipient: str, message: str) -> bool:
        self.logger.log(f"[DEBUG] Отправка уведомления {recipient}: {message}")
        # Сохраняем уведомление в данные
        self.data_service.save_data(f"notification_to_{recipient}")
        return True


class ReleaseNotificationService(INotificationService):
    def __init__(self, logger: ILogger, data_service: IDataService, smtp_server: str = "smtp.example.com"):
        self.logger = logger
        self.data_service = data_service
        self.smtp_server = smtp_server
        self.logger.log(f"ReleaseNotificationService инициализирован с SMTP: {smtp_server}")

    def send_notification(self, recipient: str, message: str) -> bool:
        self.logger.log(f"Отправка email уведомления {recipient}: {message}")
        # Сохраняем уведомление в данные
        self.data_service.save_data(f"email_sent_to_{recipient}")
        return True


# ========================= ФАБРИЧНЫЕ МЕТОДЫ =========================

def create_console_logger():
    """Фабричный метод для создания консольного логгера"""
    return DebugLogger("[CONSOLE]")


def create_file_logger():
    """Фабричный метод для создания файлового логгера"""
    return ReleaseLogger("FILE")


# ========================= КОНФИГУРАЦИИ =========================

def setup_debug_configuration(container: DIContainer):
    """Настройка debug конфигурации"""
    print("\n=== Настройка DEBUG конфигурации ===")

    # Регистрация с различными жизненными циклами
    container.register(ILogger, DebugLogger, LifeStyle.SINGLETON, prefix="[DEBUG-SINGLETON]")
    container.register(IDataService, DebugDataService, LifeStyle.SCOPED, connection_string="debug_scoped_db")
    container.register(INotificationService, DebugNotificationService, LifeStyle.PER_REQUEST)


def setup_release_configuration(container: DIContainer):
    """Настройка release конфигурации"""
    print("\n=== Настройка RELEASE конфигурации ===")

    # Регистрация с фабричными методами и параметрами
    container.register(ILogger, factory_method=create_file_logger, lifestyle=LifeStyle.SINGLETON)
    container.register(IDataService, ReleaseDataService, LifeStyle.SINGLETON, connection_string="prod_main_db")
    container.register(INotificationService, ReleaseNotificationService, LifeStyle.PER_REQUEST,
                       smtp_server="mail.company.com")


# ========================= ДЕМОНСТРАЦИЯ =========================

def demonstrate_di_container():
    """Демонстрация работы DI контейнера"""

    print("🚀 ДЕМОНСТРАЦИЯ DEPENDENCY INJECTION КОНТЕЙНЕРА\n")

    # ===== DEBUG КОНФИГУРАЦИЯ =====
    print("📋 ТЕСТИРОВАНИЕ DEBUG КОНФИГУРАЦИИ")
    debug_container = DIContainer()
    setup_debug_configuration(debug_container)

    print("\n--- Тестирование Singleton (Logger) ---")
    logger1 = debug_container.get_instance(ILogger)
    logger2 = debug_container.get_instance(ILogger)
    print(f"Singleton test: logger1 is logger2 = {logger1 is logger2}")

    print("\n--- Тестирование Scoped (DataService) ---")
    with debug_container.create_scope():
        data_service1 = debug_container.get_instance(IDataService)
        data_service2 = debug_container.get_instance(IDataService)
        print(f"Scoped test 1: data_service1 is data_service2 = {data_service1 is data_service2}")

        # Использование сервисов
        data = data_service1.get_data()
        print(f"Полученные данные: {data}")
        data_service1.save_data("новая_debug_запись")

    with debug_container.create_scope():
        data_service3 = debug_container.get_instance(IDataService)
        print(f"Scoped test 2: data_service1 is data_service3 = {data_service1 is data_service3}")

    print("\n--- Тестирование PerRequest (NotificationService) ---")
    with debug_container.create_scope():
        notification1 = debug_container.get_instance(INotificationService)
        notification2 = debug_container.get_instance(INotificationService)
        print(f"PerRequest test: notification1 is notification2 = {notification1 is notification2}")

        # Использование сервиса уведомлений
        notification1.send_notification("user@example.com", "Тестовое сообщение")

    # ===== RELEASE КОНФИГУРАЦИЯ =====
    print("\n\n📋 ТЕСТИРОВАНИЕ RELEASE КОНФИГУРАЦИИ")
    release_container = DIContainer()
    setup_release_configuration(release_container)

    print("\n--- Тестирование фабричного метода (Logger) ---")
    logger3 = release_container.get_instance(ILogger)
    logger4 = release_container.get_instance(ILogger)
    print(f"Factory method Singleton test: logger3 is logger4 = {logger3 is logger4}")

    print("\n--- Полный рабочий сценарий ---")
    # Получаем все сервисы
    logger = release_container.get_instance(ILogger)
    data_service = release_container.get_instance(IDataService)
    notification_service = release_container.get_instance(INotificationService)

    # Работаем с данными
    logger.log("Начало работы с данными")
    current_data = data_service.get_data()
    logger.log(f"Текущие данные: {current_data}")

    # Добавляем новые данные
    data_service.save_data("новая_production_запись")
    data_service.save_data("еще_одна_запись")

    # Отправляем уведомления
    notification_service.send_notification("admin@company.com", "Данные обновлены")
    notification_service.send_notification("user@company.com", "Система работает корректно")

    # Проверяем обновленные данные
    updated_data = data_service.get_data()
    logger.log(f"Обновленные данные: {updated_data}")

    print("\n✅ Демонстрация завершена успешно!")


if __name__ == "__main__":
    demonstrate_di_container()
