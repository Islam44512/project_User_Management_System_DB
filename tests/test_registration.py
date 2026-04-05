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

def test_add_existing_username(setup_database, connection):
    """Тест добавления пользователя с уже существующим логином."""
    
    add_user('existinguser', 'existing@example.com', 'password123')
    
    result = add_user('existinguser', 'another@example.com', 'differentpass')
    
    assert not result, "Добавление пользователя с существующим логином должно быть запрещено"
    
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username='existinguser';")
    users = cursor.fetchall()
    assert len(users) == 1, "В базе должен остаться только один пользователь с этим логином"


def test_successful_authentication(setup_database, connection):
    """Тест успешной аутентификации пользователя."""
    add_user('authuser', 'auth@example.com', 'correctpass')
    authenticated = authenticate_user('authuser', 'correctpass')
    assert authenticated, "Аутентификация должна пройти успешно с правильными данными"

def test_authenticate_nonexistent_user(setup_database):
    """Тест аутентификации несуществующего пользователя."""
    authenticated = authenticate_user('nonexistent', 'anypassword')
    assert not authenticated, "Аутентификация несуществующего пользователя должна завершиться ошибкой"

def test_authenticate_with_wrong_password(setup_database, connection):
    """Тест аутентификации пользователя с неправильным паролем."""
    add_user('wrongpassuser', 'wrongpass@example.com', 'correctpassword')
    authenticated = authenticate_user('wrongpassuser', 'wrongpassword')
    assert not authenticated, "Аутентификация с неправильным паролем должна завершиться ошибкой"


def test_display_users(setup_database, capsys):
    """Тест корректного отображения списка пользователей."""
    add_user('displaytest', 'displaytest@example.com', 'password123')
    display_users()
    captured = capsys.readouterr()
    assert 'displaytest' in captured.out, "Функция отображения должна выводить логины пользователей."
    assert 'password123' not in captured.out, "Пароли не должны отображаться."



# Возможные варианты тестов:
"""
Тест добавления пользователя с существующим логином.
Тест успешной аутентификации пользователя.
Тест аутентификации несуществующего пользователя.
Тест аутентификации пользователя с неправильным паролем.
Тест отображения списка пользователей.
"""