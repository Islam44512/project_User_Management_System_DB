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

# Возможные варианты тестов:
"""
Тест добавления пользователя с существующим логином.
Тест успешной аутентификации пользователя.
Тест аутентификации несуществующего пользователя.
Тест аутентификации пользователя с неправильным паролем.
Тест отображения списка пользователей.
"""

def test_add_user_with_existing_username(connection):
    """Тест добавления пользователя с существующим логином."""
    #add_user('testuser', 'testuser@example.com', 'password123')
    # with pytest.raises(sqlite3.IntegrityError):
    assert add_user('testuser', 'testuser2@example.com', 'password456') == False

def test_authenticate_user(connection):
    """Тест успешной аутентификации пользователя."""
    add_user('testuser', 'testuser@example.com', 'password123')
    assert authenticate_user('testuser', 'password123'), "Пользователь должен быть аутентифицирован."

def test_authenticate_nonexistent_user(connection):
    """Тест аутентификации несуществующего пользователя."""
    assert not authenticate_user('nonexistentuser', 'password123'), "Несуществующий пользователь не должен быть аутентифицирован."

def test_authenticate_wrong_password(connection):
    """Тест аутентификации пользователя с неправильным паролем."""
    add_user('testuser', 'testuser@example.com', 'password123')
    assert not authenticate_user('testuser', 'wrongpassword'), "Пользователь с неверным паролем не должен быть аутентифицирован."

def test_display_users(connection):
    """Тест отображения списка пользователей."""
    add_user('testuser', 'testuser@example.com', 'password123')
    users = display_users()
    # получить количество пользователей в базе данных через командку SELECT COUNT(*) FROM users
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM users")
        count = cursor.fetchone()[0]
    assert  users == count, "Список пользователей должен содержать один пользователь."