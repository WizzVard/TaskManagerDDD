from src.task_manager.domain.entities.project import Project
from src.task_manager.domain.repositories.project_repository_interface import ProjectRepositoryInterface
from src.task_manager.infrastructure.common.transaction_decorator import transactional
from src.task_manager.infrastructure.database.database_connection import DatabaseConnection
from typing import Optional, List


class ProjectRepository(ProjectRepositoryInterface):
    def __init__(self, db_connection: DatabaseConnection):
        self.db_connection = db_connection

    def get_connection(self):
        return self.db_connection.get_connection()
    
    @transactional
    async def create_project(self, project: Project, conn=None) -> Project:
        query = """
            INSERT INTO projects (name, description, created_at)
            VALUES (%s, %s, %s)
            RETURNING id, created_at;
        """
        with conn.cursor() as cursor:
            cursor.execute(query, (
                project.name,
                project.description,
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
                    created_at=row['created_at'],
                    updated_at=row['updated_at']
                )
            return None
        
    @transactional
    async def get_all_projects(self, conn=None) -> List[Project]:
        query = "SELECT * FROM projects;"
        with conn.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
            return [
                Project(
                    id=row['id'],
                    name=row['name'],
                    description=row['description'],
                    created_at=row['created_at'],
                    updated_at=row['updated_at']
                ) for row in rows
            ]
        
    @transactional
    async def update_project(self, project_id: int, project: Project, conn=None) -> Project: 
        query = """UPDATE projects 
        SET name = %s, description = %s, updated_at = %s
        WHERE id = %s
        RETURNING *;"""
        with conn.cursor() as cursor:
            cursor.execute(query, (
                project.name,
                project.description,
                project.updated_at,
                project_id
            ))
            row = cursor.fetchone()
            if row:
                return Project(
                    id=row['id'],
                    name=row['name'],
                    description=row['description'],
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
