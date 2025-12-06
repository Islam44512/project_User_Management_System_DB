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

# остальные
def test_add_user_with_existing_username(setup_database):
    """логин уже есть - тест"""
    add_user('existinguser', 'user1@example.com', 'pass1')
    result = add_user('existinguser', 'user2@example.com', 'pass2')
    assert result == False, "Нельзя добавить пользователя с существующим логином"

def test_authenticate_success(setup_database):
    """успешная аутентификация"""
    add_user('authuser', 'auth@example.com', 'authpass')
    result = authenticate_user('authuser', 'authpass')
    assert result == True, "аутентификация должна быть успешной"

def test_authenticate_wrong_password(setup_database):
    """тест неверного пароля"""
    add_user('wrongpassuser', 'wrong@example.com', 'correctpass')
    result = authenticate_user('wrongpassuser', 'wrongpass')
    assert result == False, "аутентификация должна быть неудачной"

def test_authenticate_nonexistent_user(setup_database):
    """тест несуществующего пользователя"""
    result = authenticate_user('nonexistent', 'password')
    assert result == False, "несуществующий пользователь не должен аутентифицироваться"

def test_display_users(setup_database, capsys):
    """тест списка пользователей"""
# честно скажу этот мне ии помог
    add_user('user1', 'user1@test.com', 'pass1')
    add_user('user2', 'user2@test.com', 'pass2')
    
    display_users()
    captured = capsys.readouterr()
    
    assert 'user1' in captured.out
    assert 'user2' in captured.out
    assert 'user1@test.com' in captured.out
    assert 'user2@test.com' in captured.out