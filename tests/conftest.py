import pytest
from datetime import datetime, UTC
from src.task_manager.domain.entities.task import Task
from src.core.config import Settings
from src.task_manager.infrastructure.repositories.task_repository import TaskRepository
from src.task_manager.infrastructure.repositories.google_calendar_repository import GoogleCalendarRepository
from src.task_manager.application.services.task_service import TaskService

@pytest.fixture
def test_settings():
    return Settings(
        DB_NAME="taskmanager_test",
        DB_USER="postgres",
        DB_PASS="22032004",
        DB_HOST="localhost",
        DB_PORT="5432"
    )

@pytest.fixture
def task_repository(test_settings):
    repo = TaskRepository(test_settings)
    # Clear the test database before each test
    try:
        conn = repo.get_connection()
        with conn.cursor() as cursor:
            cursor.execute("TRUNCATE tasks RESTART IDENTITY CASCADE")
        conn.commit()
    finally:
        if conn:
            conn.close()
    return repo

@pytest.fixture
def mock_calendar_client():
    class MockGoogleCalendarClient:
        async def create_event(self, task):
            pass
        async def update_event(self, task):
            pass
        async def delete_event(self, task):
            pass
    return MockGoogleCalendarClient()

@pytest.fixture
def task_service(task_repository, mock_calendar_client):
    return TaskService(task_repository, mock_calendar_client)

@pytest.fixture
def sample_task():
    return Task(
        title="Test Task",
        description="Test Description",
        deadline=datetime.now(UTC)
    )