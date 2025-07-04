# tests/test_registration.py
import os
import sqlite3
import builtins
import pytest

from registration import (
    create_db,
    add_user,
    authenticate_user,
    display_users,
    user_choice,
)

DB_PATH = "users.db"


# ──────────────────────────── фикстуры ────────────────────────────
@pytest.fixture(scope="module", autouse=True)
def fresh_db():
    """Создаём БД перед первым тестом и удаляем после всех тестов."""
    create_db()
    yield
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)


@pytest.fixture
def connection():
    conn = sqlite3.connect(DB_PATH)
    yield conn
    conn.close()


# ──────────────────────────── сами тесты ──────────────────────────
def test_table_exists(connection):
    cur = connection.cursor()
    cur.execute(
        "SELECT name FROM sqlite_master "
        "WHERE type='table' AND name='users';"
    )
    assert cur.fetchone(), "Таблица users не создана."


def test_add_user_success(connection):
    assert add_user("alice", "a@mail.com", "pass") is True
    cur = connection.cursor()
    cur.execute("SELECT username FROM users WHERE username='alice';")
    assert cur.fetchone(), "Пользователь alice не добавлен."


def test_add_user_duplicate():
    add_user("bob", "b@mail.com", "123")
    # повторная попытка должна вернуть False (PRIMARY KEY конфликт)
    assert add_user("bob", "b@mail.com", "456") is False


def test_authenticate_ok():
    add_user("charlie", "c@mail.com", "qwerty")
    assert authenticate_user("charlie", "qwerty") is True


def test_authenticate_wrong_password():
    add_user("dave", "d@mail.com", "secret")
    assert authenticate_user("dave", "wrong") is False


def test_authenticate_no_such_user():
    assert authenticate_user("ghost", "nopass") is False


def test_display_users_prints(capsys):
    # Функция ничего не возвращает, только печатает.
    add_user("eve", "e@mail.com", "pwd")
    display_users()
    captured = capsys.readouterr()
    assert "Логин:" in captured.out and "eve" in captured.out


def test_user_choice(monkeypatch):
    """Проверяем, что функция читает ввод и возвращает его."""
    monkeypatch.setattr(builtins, "input", lambda _: "2")
    assert user_choice() == "2"
