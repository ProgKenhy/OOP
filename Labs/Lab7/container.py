from enum import Enum
from typing import Dict, Any, Type, Callable, Optional, List
import inspect
import threading


class LifeStyle(Enum):
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
