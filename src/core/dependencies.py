from fastapi import Depends
from typing import Annotated
from src.task_manager.application.services.task_service import TaskService
from src.task_manager.infrastructure.repositories.task_repository import TaskRepository
from src.task_manager.infrastructure.repositories.google_calendar_repository import GoogleCalendarRepository
from src.task_manager.domain.repositories.calendar_repository_interface import CalendarRepositoryInterface
from src.core.config import Settings
from src.task_manager.domain.repositories.task_repository_interface import TaskRepositoryInterface

def get_settings() -> Settings:
    return Settings()

def get_task_repository(
    settings: Annotated[Settings, Depends(get_settings)]
) -> TaskRepository:
    return TaskRepository(settings)

def get_calendar_repository() -> CalendarRepositoryInterface:
    return GoogleCalendarRepository()

def get_task_service(
    task_repository: TaskRepositoryInterface = Depends(get_task_repository),
    calendar_repository: CalendarRepositoryInterface = Depends(get_calendar_repository)
) -> TaskService:
    return TaskService(task_repository, calendar_repository)