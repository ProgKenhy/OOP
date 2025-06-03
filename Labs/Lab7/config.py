from container import LifeStyle
from interfaces import ILogger, IDataService, INotificationService
from implementations import (
    DebugLogger, DebugDataService, DebugNotificationService,
    ReleaseDataService, ReleaseNotificationService
)
from factories import create_file_logger


def setup_debug_configuration(container):
    """Настройка debug конфигурации"""
    print("\n=== Настройка DEBUG конфигурации ===")

    container.register(
        ILogger, 
        DebugLogger, 
        LifeStyle.SINGLETON, 
        prefix="[DEBUG-SINGLETON]"
    )
    container.register(
        IDataService, 
        DebugDataService, 
        LifeStyle.SCOPED, 
        connection_string="debug_scoped_db"
    )
    container.register(
        INotificationService, 
        DebugNotificationService, 
        LifeStyle.PER_REQUEST
    )


def setup_release_configuration(container):
    """Настройка release конфигурации"""
    print("\n=== Настройка RELEASE конфигурации ===")

    container.register(
        ILogger, 
        factory_method=create_file_logger, 
        lifestyle=LifeStyle.SINGLETON
    )
    container.register(
        IDataService, 
        ReleaseDataService, 
        LifeStyle.SINGLETON, 
        connection_string="prod_main_db"
    )
    container.register(
        INotificationService, 
        ReleaseNotificationService, 
        LifeStyle.PER_REQUEST,
        smtp_server="mail.company.com"
    )
