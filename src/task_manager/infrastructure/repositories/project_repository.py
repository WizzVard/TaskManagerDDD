from src.task_manager.domain.entities.project import Project
from src.task_manager.domain.entities.task import Task
from src.task_manager.domain.repositories.project_repository_interface import ProjectRepositoryInterface
from src.task_manager.infrastructure.common.transaction_decorator import transactional
from src.task_manager.infrastructure.database.database_connection import DatabaseConnection
from typing import Optional, List, Tuple, Dict


class ProjectRepository(ProjectRepositoryInterface):
    def __init__(self, db_connection: DatabaseConnection):
        self.db_connection = db_connection

    def get_connection(self):
        return self.db_connection.get_connection()
    
    @transactional
    async def create_project(self, project: Project, conn=None) -> Project:
        query = """
            INSERT INTO projects (name, description, color, created_at)
            VALUES (%s, %s, %s, %s)
            RETURNING id, created_at;
        """
        with conn.cursor() as cursor:
            cursor.execute(query, (
                project.name,
                project.description,
                project.color,
                project.created_at
            ))
            result = cursor.fetchone()
            project.id = result[0]
            project.created_at = result[1]
            return project
    
    @transactional
    async def get_project_by_id(self, project_id: int, conn=None) -> Optional[Project]:
        query = """SELECT * FROM projects WHERE id = %s;"""
        with conn.cursor() as cursor:
            cursor.execute(query, (project_id,))
            row = cursor.fetchone()
            if row:
                return Project(
                    id=row['id'],
                    name=row['name'],
                    description=row['description'],
                    color=row['color'],
                    created_at=row['created_at'],
                    updated_at=row['updated_at']
                )
            return None
        
    @transactional
    async def get_all_projects_with_tasks(self, conn=None) -> List[Tuple[Project, List[Task]]]:
        # Получаем все проекты
        projects_query = """
            SELECT id, name, description, color, created_at, updated_at 
            FROM projects
            ORDER BY created_at DESC;
        """
        with conn.cursor() as cursor:
            cursor.execute(projects_query)
            project_rows = cursor.fetchall()

            # Получаем все задачи для этих проектов
            if project_rows:
                project_ids = [row['id'] for row in project_rows]
                placeholders = ','.join(['%s'] * len(project_ids))
                tasks_query = f"""
                    SELECT id, title, description, status, deadline, 
                           project_id, created_at, updated_at, calendar_event_id
                    FROM tasks 
                    WHERE project_id IN ({placeholders})
                    ORDER BY created_at DESC;
                """
                cursor.execute(tasks_query, project_ids)
                task_rows = cursor.fetchall()

                tasks_by_project = {}
                for row in task_rows:
                    project_id = row['project_id']
                    if project_id not in tasks_by_project:
                        tasks_by_project[project_id] = []

                    tasks_by_project[project_id].append(
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
                        )
                    )

            result = []
            for row in project_rows:
                project = Project(
                    id=row['id'],
                    name=row['name'],
                    description=row['description'],
                    color=row['color'],
                    created_at=row['created_at'],
                    updated_at=row['updated_at']
                )
                tasks = tasks_by_project.get(row['id'], [])
                result.append((project, tasks))

            return result
        
    @transactional
    async def update_project(self, project_id: int, project: Project, conn=None) -> Project: 
        query = """
            UPDATE projects 
            SET name = %s, description = %s, color = %s, 
                updated_at = CURRENT_TIMESTAMP
            WHERE id = %s
            RETURNING *;
        """
        with conn.cursor() as cursor:
            cursor.execute(query, (
                project.name,
                project.description,
                project.color,
                project_id
            ))
            row = cursor.fetchone()
            if row:
                return Project(
                    id=row['id'],
                    name=row['name'],
                    description=row['description'],
                    color=row['color'],
                    created_at=row['created_at'],
                    updated_at=row['updated_at']
                )
            return None
        
    @transactional
    async def delete_project(self, project_id: int, conn=None) -> bool:
        query = """DELETE FROM projects WHERE id = %s;"""
        with conn.cursor() as cursor:
            cursor.execute(query, (project_id,))
            return cursor.rowcount > 0
        
    @transactional
    async def delete_all_projects(self, conn=None) -> bool:
        query = "DELETE FROM projects;"
        with conn.cursor() as cursor:
            cursor.execute(query)
            return cursor.rowcount > 0
