from typing import List, Optional
from src.task_manager.domain.entities.task import Task
from src.task_manager.domain.repositories.task_repository_interface import TaskRepositoryInterface
from src.task_manager.infrastructure.common.transaction_decorator import transactional
from src.task_manager.infrastructure.database.database_connection import DatabaseConnection


class TaskRepository(TaskRepositoryInterface):
    def __init__(self, db_connection: DatabaseConnection):
        self.db_connection = db_connection

    def get_connection(self):
        return self.db_connection.get_connection()
    
    @transactional
    async def create_task(self, task: Task, conn=None) -> Task:
        query = """
            INSERT INTO tasks (title, description, status, deadline, 
                project_id, created_at, calendar_event_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id, created_at, calendar_event_id;
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
            task.calendar_event_id = result[2]
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
                    updated_at=row['updated_at'],
                    calendar_event_id=row['calendar_event_id']
                )
            return None
        
    @transactional
    async def get_tasks_by_project(self, project_id: str, conn=None) -> List[Task]:
        query = "SELECT * FROM tasks WHERE project_id = %s;"
        with conn.cursor() as cursor:
            cursor.execute(query, (project_id,))
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
                    updated_at=row['updated_at'],
                    calendar_event_id=row['calendar_event_id']
                ) for row in rows
            ]

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
        
    @transactional
    async def delete_all_tasks(self, conn=None) -> bool:
        query = "DELETE FROM tasks;"
        with conn.cursor() as cursor:
            cursor.execute(query)
            return cursor.rowcount > 0

