from functools import wraps
import psycopg2
import psycopg2.extras
from typing import List, Optional
from src.task_manager.domain.entities.task import Task
from src.core.config import Settings

def transactional(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        db_instance = args[0]  # self
        conn = None
        try:
            conn = db_instance.get_connection()
            result = await func(*args, conn=conn, **kwargs)
            conn.commit()
            return result
        except Exception as e:
            if conn:
                conn.rollback()
            print(f"Error in transaction: {e}")
            raise
        finally:
            if conn:
                conn.close()
    return wrapper

class TaskRepository:
    def __init__(self, settings: Settings):
        self.settings = settings

    def get_connection(self):
        try:
            conn = psycopg2.connect(
                dbname=self.settings.DB_NAME,
                user=self.settings.DB_USER,
                password=self.settings.DB_PASS,
                host=self.settings.DB_HOST,
                port=self.settings.DB_PORT
            )
            conn.cursor_factory = psycopg2.extras.DictCursor
            return conn
        except Exception as e:
            print(f"Error connecting to database: {e}")
            raise

    @transactional
    async def create_task(self, task: Task, conn=None) -> Task:
        query = """
            INSERT INTO tasks (
                title, description, status, deadline, 
                project_id, created_at, calendar_event_id
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id, created_at;
        """
        with conn.cursor() as cursor:
            cursor.execute(query, (
                task.title,
                task.description,
                task.status,
                task.deadline,
                task.project_id,
                task.created_at,
                task.calendar_event_id
            ))
            result = cursor.fetchone()
            task.id = result[0]
            task.created_at = result[1]
            return task

    @transactional
    async def get_task_by_id(self, task_id: int, conn=None) -> Optional[Task]:
        query = "SELECT * FROM tasks WHERE id = %s;"
        with conn.cursor() as cursor:
            cursor.execute(query, (task_id,))
            row = cursor.fetchone()
            if row:
                return Task(
                    id=row['id'],
                    title=row['title'],
                    description=row['description'],
                    status=row['status'],
                    deadline=row['deadline'],
                    project_id=row['project_id'],
                    created_at=row['created_at'],
                    updated_at=row['updated_at']
                )
            return None

    @transactional
    async def get_all_tasks(self, conn=None) -> List[Task]:
        query = "SELECT * FROM tasks;"
        with conn.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
            return [
                Task(
                    id=row['id'],
                    title=row['title'],
                    description=row['description'],
                    status=row['status'],
                    deadline=row['deadline'],
                    project_id=row['project_id'],
                    created_at=row['created_at'],
                    updated_at=row['updated_at']
                ) for row in rows
            ]

    @transactional
    async def update_task(self, task_id: int, task: Task, conn=None) -> Optional[Task]:
        query = """
            UPDATE tasks 
            SET title = %s, description = %s, status = %s, 
                deadline = %s, project_id = %s, calendar_event_id = %s 
            WHERE id = %s 
            RETURNING *;
        """
        with conn.cursor() as cursor:
            cursor.execute(query, (
                task.title,
                task.description,
                task.status,
                task.deadline,
                task.project_id,
                task.calendar_event_id,
                task_id
            ))
            row = cursor.fetchone()
            if row:
                return Task(
                    id=row['id'],
                    title=row['title'],
                    description=row['description'],
                    status=row['status'],
                    deadline=row['deadline'],
                    project_id=row['project_id'],
                    created_at=row['created_at'],
                    updated_at=row['updated_at'],
                    calendar_event_id=row['calendar_event_id']
                )
            return None

    @transactional
    async def delete_task(self, task_id: int, conn=None) -> bool:
        query = "DELETE FROM tasks WHERE id = %s;"
        with conn.cursor() as cursor:
            cursor.execute(query, (task_id,))
            return cursor.rowcount > 0

