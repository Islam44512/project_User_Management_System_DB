import pytest
import sqlite3
import os
from registration.registration import create_db, add_user, authenticate_user, display_users

@pytest.fixture(scope="module")
def setup_database():
    """Фикстура для настройки базы данных перед тестами и её очистки после."""
    create_db()
    yield
    try:
        os.remove('users.db')
    except PermissionError:
        pass

@pytest.fixture
def connection():
    """Фикстура для получения соединения с базой данных и его закрытия после теста."""
    conn = sqlite3.connect('users.db')
    yield conn
    conn.close()


def test_create_db(setup_database, connection):
    """Тест создания базы данных и таблицы пользователей."""
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
    table_exists = cursor.fetchone()
    assert table_exists, "Таблица 'users' должна существовать в базе данных."

def test_add_new_user(setup_database, connection):
    """Тест добавления нового пользователя."""
    add_user('testuser', 'testuser@example.com', 'password123')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username='testuser';")
    user = cursor.fetchone()
    assert user, "Пользователь должен быть добавлен в базу данных."
    assert user[1] == 'testuser@example.com', "Email должен совпадать"
    assert user[2] == 'password123', "Пароль должен совпадать"

# Возможные варианты тестов:
"""
Тест добавления пользователя с существующим логином.
Тест успешной аутентификации пользователя.
Тест аутентификации несуществующего пользователя.
Тест аутентификации пользователя с неправильным паролем.
Тест отображения списка пользователей.
"""


def test_add_user_existing_username(setup_database, connection):
    """Тест добавления пользователя с существующим логином."""
    add_user('existing_user', 'first@example.com', 'pass123')
    result = add_user('existing_user', 'second@example.com', 'pass1234')
    assert result is False


def test_authenticate_user_success(setup_database, connection):
    """Тест успешной аутентификации пользователя."""
    add_user('auth_user', 'auth@example.com', 'correct_password')
    result = authenticate_user('auth_user', 'correct_password')
    assert result is True


def test_authenticate_user_nonexistent(setup_database):
    """Тест аутентификации несуществующего пользователя."""
    result = authenticate_user('nonexistent_user', 'any_password')
    
    assert result is False
