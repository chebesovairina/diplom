from config import *

# Настройка контекста для хеширования паролей
pwd_context = CryptContext(
    schemes=["pbkdf2_sha256"],
    default="pbkdf2_sha256",
    pbkdf2_sha256__default_rounds=30000
)

def print_users_table():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    # Получаем все записи из таблицы users
    cursor.execute('SELECT id, avatar, login, password FROM users')
    users = cursor.fetchall()
    if not users:
        print("Таблица users пуста.")
        return
    # Выводим заголовок таблицы
    print("\nСодержимое таблицы users:")
    print("-" * 80)
    print(f"| {'ID':<3} | {'Avatar':<12} | {'Login':<20} | {'Password (hashed)':<100} |")
    print("-" * 80)
    # Выводим каждую запись
    for user in users:
        user_id, avatar, login, password_hash = user
        # Обрезаем хеш для удобства просмотра (первые 16 символов + ...)
        truncated_hash = (password_hash[:16] + '...') if len(password_hash) > 16 else password_hash
        print(f"| {user_id:<3} | {avatar:<12} | {login:<20} | {password_hash:<100} |")
    print("-" * 80)
    print(f"Всего пользователей: {len(users)}")
    conn.close()

def print_user_vacancies():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM user_vacancies')
    user = cursor.fetchone()
    conn.close()
    print(user)

def init_db():
    # Подключение к базе данных (создание файла, если его нет)
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    # Создание таблицы пользователя
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            avatar TEXT DEFAULT 'avatar1.png',      -- Имя файла аватарки
            login TEXT NOT NULL,                    -- Логин пользователя
            password TEXT NOT NULL                  -- Пароль пользователя
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_vacancies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            job_titles TEXT,      -- Названия вакансий
            companies TEXT,       -- Компании
            skills TEXT,          -- Навыки и технологии
            languages TEXT,       -- Иностранные языки
            other TEXT,           -- Другие ключевые слова
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    ''')
    # Сохранение изменений и закрытие подключения
    conn.commit()
    conn.close()


def add_data(login, password):
    # Хешируем пароль перед сохранением
    hashed_password = pwd_context.hash(password)
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO users (login, password)
        VALUES (?, ?)
    ''', (login, hashed_password))
    conn.commit()
    conn.close()


def check_data(login):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM users WHERE login = ?', (login,))
    user = cursor.fetchone()
    conn.close()
    return user


def check_login(login, password):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    # Получаем хеш пароля из БД по логину
    cursor.execute('SELECT id, password FROM users WHERE login = ?', (login,))
    user_data = cursor.fetchone()
    conn.close()
    if user_data:
        user_id, hashed_password = user_data
        # Проверяем, соответствует ли пароль хешу
        if pwd_context.verify(password, hashed_password):
            return user_id
    return None


def get_current_avatar():
    user_id = str(session.get('user_id', ''))
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    user = cursor.execute("SELECT avatar FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    avatar = user[0] if user[0] else None
    return avatar


def update_avatar(user_id, avatar_filename):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET avatar = ? WHERE id = ?", (avatar_filename, user_id))
    conn.commit()
    conn.close()
