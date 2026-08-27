import pytest
import sqlite3
import os
from registration.registration import add_user, authenticate_user, display_users, create_db

@pytest.fixture
def connection():
    """Фикстура для получения соединения с базой данных и его закрытия после теста."""
    conn = sqlite3.connect('users.db')
    yield conn
    conn.close()

@pytest.fixture
def setup_database():
    create_db()
    yield

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

def test_add_existing_user(setup_database):
    """Тест попытки добавления пользователя с существующим логином."""
    add_user('existinguser', 'existinguser@example.com', 'password123')
    response = add_user('existinguser', 'existinguser2@example.com', 'password1234')
    assert not response, "Пользователь с существующим логином не должен сохраняться."

def test_authenticate_user_success(setup_database):
    """Тест успешной аутентификации пользователя."""
    add_user('testauth', 'testauth@example.com', 'password123')
    assert authenticate_user('testauth', 'password123') == True

def test_authenticate_nonexistent_user(setup_database):
    """Тест аутентификации несуществующего пользователя."""
    assert authenticate_user('nonexistentuser', 'password') == False

def test_authenticate_user_wrong_password(setup_database):
    """Тест аутентификации пользователя с неправильным паролем."""
    add_user('wrongpass', 'wrongpass@example.com', 'password123')
    assert authenticate_user('wrongpass', 'wrongpassword') == False

def test_display_users(setup_database, capsys):
    """Тест корректного отображения списка пользователей."""
    add_user('displaytest', 'displaytest@example.com', 'password123')
    display_users()
    captured = capsys.readouterr()
    assert 'displaytest' in captured.out, "Функция отображения должна выводить логины пользователей."
    assert 'password123' not in captured.out, "Пароли не должны отображаться."