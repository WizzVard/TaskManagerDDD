import psycopg2
from src.core.config import Settings

def setup_test_db():
    # Первое соединение для создания БД
    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        dbname="postgres",
        user="postgres",
        password="22032004",
        client_encoding='utf8'
    )
    conn.autocommit = True

    with conn.cursor() as cursor:
        # Закрываем активные соединения
        cursor.execute("""
            SELECT pg_terminate_backend(pg_stat_activity.pid)
            FROM pg_stat_activity
            WHERE pg_stat_activity.datname = 'taskmanager_test'
            AND pid <> pg_backend_pid();
        """)
        
        # Удаляем БД если существует
        cursor.execute("DROP DATABASE IF EXISTS taskmanager_test")
        
        # Создаем БД
        cursor.execute("""
            CREATE DATABASE taskmanager_test
            TEMPLATE template0
            LC_COLLATE 'Russian_Russia.1251'
            LC_CTYPE 'Russian_Russia.1251'
            ENCODING 'WIN1251'
        """)
    
    conn.close()

    # Второе соединение для создания таблиц
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
            # Создаем таблицу projects первой
            cursor.execute("""
                CREATE TABLE projects (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    description TEXT,
                    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP WITH TIME ZONE,
                    task_count INTEGER NOT NULL DEFAULT 0
                );
            """)

            # Затем создаем tasks с внешним ключом
            cursor.execute("""
                CREATE TABLE tasks (
                    id SERIAL PRIMARY KEY,
                    title VARCHAR(100) NOT NULL,
                    description TEXT,
                    status VARCHAR(20) NOT NULL DEFAULT 'NEW',
                    deadline TIMESTAMP WITH TIME ZONE,
                    project_id INTEGER REFERENCES projects(id),
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