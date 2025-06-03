from config import setup_debug_configuration, setup_release_configuration
from container import DIContainer
from interfaces import ILogger, IDataService, INotificationService


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
