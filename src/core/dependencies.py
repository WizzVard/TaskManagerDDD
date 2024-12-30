from fastapi import Depends
from typing import Annotated
from src.task_manager.application.services.task_service import TaskService
from src.task_manager.infrastructure.repositories.task_repository import TaskRepository
from src.task_manager.infrastructure.external_services.google_calendar_client import GoogleCalendarClient
from src.core.config import Settings

def get_settings() -> Settings:
    return Settings()

def get_task_repository(
    settings: Annotated[Settings, Depends(get_settings)]
) -> TaskRepository:
    return TaskRepository(settings)

def get_calendar_client() -> GoogleCalendarClient:
    return GoogleCalendarClient()  # или с нужными параметрами

def get_task_service(
    repository: TaskRepository = Depends(get_task_repository),
    calendar_client: GoogleCalendarClient = Depends(get_calendar_client)
) -> TaskService:
    return TaskService(repository, calendar_client)