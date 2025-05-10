import pytest
import sqlite3
import os
from registration.registration import create_db, add_user, authenticate_user  # Укажите правильный путь к вашему модулю

TEST_DB_NAME = "test_users.db"  # Имя тестовой базы данных

def setup_database():
    """Фикстура для настройки базы данных перед каждым тестом и её очистки после."""
    create_db()  # Убираем аргумент
    yield
    try:
        os.remove(TEST_DB_NAME) #Удаляем конкретный файл, а не users.db
    except PermissionError:
        print(f"Не удалось удалить базу данных users.db. Возможно, она используется другим процессом.")


@pytest.fixture
def connection():
    """Фикстура для получения соединения с базой данных и его закрытия после теста."""
    conn = sqlite3.connect(TEST_DB_NAME) #Подключаемся к конкретному файлу, а не к тестовому
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
    add_user('testuser', 'testuser@example.com', 'password123') # Убираем аргумент
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username='testuser';")
    user = cursor.fetchone()
    assert user, "Пользователь должен быть добавлен в базу данных."

def test_add_user_duplicate(setup_database, connection):
    """Тест добавления пользователя с существующим логином."""
    add_user('testuser', 'testuser@example.com', 'password123')
    result = add_user('testuser', 'another@example.com', 'newpassword')
    assert result == False, "Добавлен дубликат пользователя."

def test_authenticate_user_success(setup_database, connection):
    """Тест успешной аутентификации пользователя."""
    add_user('testuser', 'testuser@example.com', 'password123')
    is_authenticated = authenticate_user('testuser', 'password123')
    assert is_authenticated, "Аутентификация должна быть успешной."

def test_authenticate_user_failure(setup_database, connection):
    """Тест аутентификации с неверным логином или паролем."""
    add_user('testuser', 'testuser@example.com', 'password123')
    is_authenticated = authenticate_user('testuser', 'wrongpassword')
    assert not is_authenticated, "Аутентификация не должна быть успешной с неверным паролем."
    is_authenticated = authenticate_user('wronguser', 'password123')
    assert not is_authenticated, "Аутентификация не должна быть успешной с неверным логином."