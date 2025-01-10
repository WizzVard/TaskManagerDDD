from src.task_manager.domain.entities.project import Project
from src.task_manager.domain.repositories.project_repository_interface import ProjectRepositoryInterface
from src.task_manager.infrastructure.common.transaction_decorator import transactional
from src.task_manager.infrastructure.database.database_connection import DatabaseConnection


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