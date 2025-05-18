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

def test_add_new_user_with_login(username):
    """Тест добавления пользователя с существующим логином."""
    add_user("testuser", "testuser@example.com", "password123")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username= ?", (username,))
    return cursor.fetchone() is not None
    
def authenticate_user(conn, username, password):
    """Тест успешной аутентификации пользователя."""
    cursor = conn.cursor()
    cursor.execute("SELECT password * FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    if result is None:
        return False
    check_password = result[0]
    return check_password == password