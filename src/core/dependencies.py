from fastapi import Depends
from typing import Annotated
from src.task_manager.application.services.task_service import TaskService
from src.task_manager.application.services.project_service import ProjectService
from src.task_manager.infrastructure.repositories.task_repository import TaskRepository
from src.task_manager.infrastructure.repositories.project_repository import ProjectRepository

from src.task_manager.infrastructure.repositories.google_calendar_repository import GoogleCalendarRepository
from src.task_manager.domain.repositories.calendar_repository_interface import CalendarRepositoryInterface
from src.core.config import Settings
from src.task_manager.domain.repositories.task_repository_interface import TaskRepositoryInterface
from src.task_manager.domain.repositories.project_repository_interface import ProjectRepositoryInterface
from src.task_manager.infrastructure.database.database_connection import DatabaseConnection

def get_settings() -> Settings:
    return Settings()

def get_db_connection(
    settings: Annotated[Settings, Depends(get_settings)]
) -> DatabaseConnection:
    return DatabaseConnection(settings)

def get_task_repository(
    db_connection: Annotated[DatabaseConnection, Depends(get_db_connection)]
) -> TaskRepository:
    return TaskRepository(db_connection)

def get_project_repository(
    db_connection: Annotated[DatabaseConnection, Depends(get_db_connection)]
) -> ProjectRepository:
    return ProjectRepository(db_connection)

def get_calendar_repository() -> CalendarRepositoryInterface:
    return GoogleCalendarRepository()

def get_task_service(
    task_repository: TaskRepositoryInterface = Depends(get_task_repository),
    calendar_repository: CalendarRepositoryInterface = Depends(get_calendar_repository),
    project_repository: ProjectRepositoryInterface = Depends(get_project_repository)
) -> TaskService:
    return TaskService(task_repository, calendar_repository, project_repository)

def get_project_service(
        project_repository: ProjectRepositoryInterface = Depends(get_project_repository),
        task_repository: TaskRepositoryInterface = Depends(get_task_repository),
        calendar_repository: CalendarRepositoryInterface = Depends(get_calendar_repository)
) -> ProjectService:
    return ProjectService(project_repository, task_repository, calendar_repository)