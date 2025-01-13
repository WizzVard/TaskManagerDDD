import psycopg2
import psycopg2.extras
from src.core.config import Settings

def check_database():
    settings = Settings()
    try:
        conn = psycopg2.connect(
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            dbname=settings.DB_NAME,
            user=settings.DB_USER,
            password=settings.DB_PASS
        )
        conn.cursor_factory = psycopg2.extras.DictCursor
        
        with conn.cursor() as cursor:
            # Проверяем структуру таблицы
            cursor.execute("""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = 'tasks';
            """)
            print("\nСтруктура таблицы tasks:")
            for row in cursor.fetchall():
                print(f"{row['column_name']}: {row['data_type']}")
            
            # Проверяем данные в таблице
            cursor.execute("SELECT * FROM tasks;")
            print("\nСодержимое таблицы tasks:")
            for row in cursor.fetchall():
                print(dict(row))
            
    except Exception as e:
        print(f"Ошибка при проверке базы данных: {e}")
    finally:
        if conn:
            conn.close()

def insert_test_task():
    settings = Settings()
    conn = psycopg2.connect(
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        dbname=settings.DB_NAME,
        user=settings.DB_USER,
        password=settings.DB_PASS
    )
    try:
        with conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO tasks (title, description, status, created_at)
                    VALUES ('Test Task', 'Test Description', 'NEW', CURRENT_TIMESTAMP)
                    RETURNING id;
                """)
                task_id = cursor.fetchone()[0]
                print(f"Created test task with ID: {task_id}")
        conn.commit()
    except Exception as e:
        print(f"Error inserting test task: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    insert_test_task()
    check_database() 