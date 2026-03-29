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


def test_add_duplicate_user(setup_database):
    """1. Тест добавления пользователя с существующим логином."""
    add_user('unique_bob', 'bob@test.com', 'pass1')
    # Повторная попытка с тем же логином должна вернуть False (из-за PRIMARY KEY)
    result = add_user('unique_bob', 'new_bob@test.com', 'pass2')
    assert result is False, "Функция должна возвращать False при попытке дублирования логина."

def test_authenticate_success(setup_database):
    """2. Тест успешной аутентификации пользователя."""
    add_user('auth_user', 'auth@test.com', 'secret123')
    result = authenticate_user('auth_user', 'secret123')
    assert result is True, "Аутентификация должна быть успешной при верных данных."

def test_authenticate_nonexistent_user(setup_database):
    """3. Тест аутентификации несуществующего пользователя."""
    result = authenticate_user('phantom_user', 'any_pass')
    assert result is False, "Аутентификация несуществующего пользователя должна возвращать False."

def test_authenticate_wrong_password(setup_database):
    """4. Тест аутентификации пользователя с неправильным паролем."""
    add_user('pass_test', 'pass@test.com', 'correct_pass')
    result = authenticate_user('pass_test', 'wrong_pass')
    assert result is False, "Аутентификация должна провалиться при неверном пароле."

def test_display_users(setup_database, capsys):
    """5. Тест отображения списка пользователей (проверка вывода в консоль)."""
    add_user('alice', 'alice@example.com', '123')
    
display_users()
# Возможные варианты тестов:
"""




Тест успешной аутентификации пользователя.
Тест аутентификации несуществующего пользователя.


"""