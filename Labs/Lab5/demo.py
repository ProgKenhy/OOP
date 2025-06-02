from models.user import User
from repositories.user_repository import UserRepository
from services.auth_service import AuthService


def demo():
    user_repo = UserRepository('storage/users.json')
    auth_service = AuthService(user_repo)

    print("1. Добавление пользователей")
    user1 = User(id=1, name="Alice", login="alice", password="pass123", email="alice@example.com")
    user2 = User(id=2, name="Bob", login="bob", password="bobpass", address="123 Main St")
    user_repo.add(user1)
    user_repo.add(user2)

    print("\nВсе пользователи (отсортировано по имени):")
    for user in sorted(user_repo.get_all()):
        print(user)

    print("\n2. Авторизация пользователя")
    auth_service.sign_in(user1)
    print(f"Текущий пользователь: {auth_service.current_user}")
    print(f"Авторизован: {auth_service.is_authorized}")

    print("\n3. Обновление пользователя")
    updated_user = User(id=1, name="Alice Smith", login="alice", password="newpass", email="alice.smith@example.com")
    user_repo.update(updated_user)
    print(f"Обновленный пользователь: {user_repo.get_by_id(1)}")

    print("\n4. Смена пользователя")
    auth_service.sign_in(user_repo.get_by_login("bob"))
    print(f"Текущий пользователь: {auth_service.current_user}")

    print("\n5. Выход из системы")
    auth_service.sign_out()
    print(f"Авторизован: {auth_service.is_authorized}")

    print("\n6. Автоматическая авторизация при новом запуске")
    print("Создаем новый экземпляр AuthService (имитация нового запуска программы)")
    new_auth_service = AuthService(user_repo)
    print(f"Авторизован автоматически: {new_auth_service.is_authorized}")
    print(f"Текущий пользователь: {new_auth_service.current_user}")


if __name__ == "__main__":
    demo()
