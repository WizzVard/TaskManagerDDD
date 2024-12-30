import psycopg2
from src.core.config import Settings

def setup_test_db():
    # Подключаемся к postgres для создания тестовой БД
    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        dbname="postgres",
        user="postgres",
        password="22032004",
        client_encoding='utf8'
    )
    conn.autocommit = True

    try:
        with conn.cursor() as cursor:
            # Удаляем БД если существует
            cursor.execute("DROP DATABASE IF EXISTS taskmanager_test")
            
            # Создаем тестовую БД
            cursor.execute("""
                CREATE DATABASE taskmanager_test
                WITH ENCODING 'UTF8'
                LC_COLLATE='en_US.UTF-8'
                LC_CTYPE='en_US.UTF-8';
            """)
    finally:
        conn.close()

    # Подключаемся к тестовой БД для создания таблиц
    settings = Settings(DB_NAME="taskmanager_test")
    conn = psycopg2.connect(
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        dbname=settings.DB_NAME,
        user=settings.DB_USER,
        password=settings.DB_PASS,
        client_encoding='utf8'
    )

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE tasks (
                    id SERIAL PRIMARY KEY,
                    title VARCHAR(100) NOT NULL,
                    description TEXT,
                    status VARCHAR(20) NOT NULL DEFAULT 'NEW',
                    deadline TIMESTAMP WITH TIME ZONE,
                    project_id INTEGER,
                    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP WITH TIME ZONE,
                    calendar_event_id VARCHAR(100)
                );
            """)
        conn.commit()
    finally:
        conn.close()

if __name__ == "__main__":
    setup_test_db() 