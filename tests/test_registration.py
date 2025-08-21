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


def test_create_db(setup_database, connection: sqlite3.Connection):
    """Тест создания базы данных и таблицы пользователей."""
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
    table_exists = cursor.fetchone()
    assert table_exists, "Таблица 'users' должна существовать в базе данных."

def test_add_new_user(setup_database, connection: sqlite3.Connection):
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
def test_new_user_exist(setup_database):
    add_user('testuser', 'testuser@example.com', 'password123')
    result = add_user('testuser', 'testuser@example1.com', 'password1234')
    assert result == False, 'Такой полбзователь уже есть'

def test_new_user_succsesufuly(setup_database):
    add_user('test','test@e.com','123')
    user = authenticate_user('test','123')
    assert user == True, 'пользователь авторизирован'

def test_authenticate_no_user(setup_database):
    result = authenticate_user('tests','1234')
    assert result == False, 'function will return False, when where is no users'

def test_authenticate_bad_password(setup_database):
    add_user('testis','test@e.com','12345')
    result = authenticate_user('testis','1234')
    assert result == False, 'function will return False, when where is bad password'

# test_display_users done with ChatGPT because I don't know how to do it xd
def test_display_users(setup_database, capsys):
    add_user('test.py','test@ee.com','123456')
    display_users()
    captured = capsys.readouterr()
    assert "Логин: test.py, Электронная почта: test@ee.com" in captured.out