import pytest
import sqlite3
import os
from registration.registration import create_db, add_user, authenticate_user, display_users


@pytest.fixture(scope="module", autouse=True)
def setup_database():
    """Создаёт базу данных перед тестами и удаляет после выполнения всех тестов."""
    create_db()
    yield
    try:
        os.remove('users.db')
    except PermissionError:
        pass


@pytest.fixture
def connection():
    """Соединение с базой данных для проверки результатов."""
    conn = sqlite3.connect('users.db')
    yield conn
    conn.close()


def test_create_db(connection):
    """Проверка, что таблица 'users' создаётся успешно."""
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
    assert cursor.fetchone() is not None, "Таблица 'users' должна существовать."


def test_add_new_user(connection):
    """Добавление нового пользователя."""
    add_user('testuser', 'testuser@example.com', 'password123')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username='testuser';")
    user = cursor.fetchone()
    assert user is not None, "Пользователь должен быть добавлен в базу данных."


def test_add_existing_user(connection):
    """Попытка добавить пользователя с уже существующим логином."""
    add_user('existinguser', 'existing@example.com', '123')
    result = add_user('existinguser', 'duplicate@example.com', '321')
    assert result is False, "Функция должна возвращать False при добавлении существующего пользователя."


def test_authenticate_valid_user(connection):
    """Проверка успешной аутентификации существующего пользователя."""
    add_user('loginuser', 'login@example.com', 'mypassword')
    result = authenticate_user('loginuser', 'mypassword')
    assert result is True, "Аутентификация должна пройти успешно для верного логина и пароля."


def test_authenticate_wrong_password(connection):
    """Проверка аутентификации с неправильным паролем."""
    add_user('wrongpass', 'wp@example.com', '12345')
    result = authenticate_user('wrongpass', 'wrong')
    assert result is False, "Аутентификация должна возвращать False при неверном пароле."


def test_authenticate_nonexistent_user():
    """Проверка аутентификации несуществующего пользователя."""
    result = authenticate_user('nouser', 'nopass')
    assert result is False, "Не должно быть успешной аутентификации несуществующего пользователя."

