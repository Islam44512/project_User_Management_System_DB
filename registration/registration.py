import sqlite3

DB_NAME = 'users.db'

def create_db():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                email TEXT NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        conn.commit()

def add_user(username, email, password):
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)', (username, email, password))
            conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def authenticate_user(username, password):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
        return cursor.fetchone() is not None

def display_users():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT username, email FROM users')
        for user in cursor.fetchall():
            print(f"Логин: {user[0]}, Электронная почта: {user[1]}")

def remove_user(username):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM users WHERE username = ?', (username,))
        conn.commit()
        return cursor.rowcount > 0

def user_choice():
    print("\n1. Авторизоваться")
    print("2. Зарегистрироваться")
    print("3. Удалить пользователя")
    choice = input("Введите ваш выбор (1/2/3): ")
    return choice

def main():
    create_db()
    display_users()

    choice = user_choice()

    if choice == '1':
        username = input("Введите логин: ")
        password = input("Введите пароль: ")
        if authenticate_user(username, password):
            print("Авторизация успешна.")
        else:
            print("Неверный логин или пароль.")
    elif choice == '2':
        username = input("Введите логин нового пользователя: ")
        email = input("Введите адрес электронной почты нового пользователя: ")
        password = input("Введите пароль нового пользователя: ")
        if add_user(username, email, password):
            print("Пользователь успешно зарегистрирован.")
        else:
            print("Пользователь с таким логином уже существует.")
    elif choice == '3':
        username = input("Введите логин пользователя для удаления: ")
        if remove_user(username):
            print(f"Пользователь '{username}' удалён.")
        else:
            print(f"Пользователь '{username}' не найден.")
    else:
        print("Неверный ввод! Пожалуйста, введите 1, 2 или 3.")

if __name__ == "__main__":
    main()
