from src.task_manager.infrastructure.repositories.google_calendar_repository import GoogleCalendarRepository
from src.task_manager.infrastructure.repositories.calendar_service import get_calendar_service
from src.task_manager.infrastructure.repositories.task_repository import TaskRepository
from src.task_manager.infrastructure.repositories.project_repository import ProjectRepository
from src.task_manager.infrastructure.database.database_connection import DatabaseConnection
from src.core.config import Settings

async def clean_calendar():
    settings = Settings()
    db_connection = DatabaseConnection(settings)
    task_repository = TaskRepository(db_connection)
    project_repository = ProjectRepository(db_connection)
    
    # Очистка базы данных
    print("\nCleaning database...")
    try:
        await task_repository.delete_all_tasks()
        await project_repository.delete_all_projects()
        print("Successfully cleaned database")
    except Exception as e:
        print(f"Error cleaning database: {e}")


    calendar_service = get_calendar_service()
    calendar_repository = GoogleCalendarRepository()
    
    # Получаем все события
    events_result = calendar_service.events().list(
        calendarId='primary',
        timeMin='2024-01-01T00:00:00Z',  # начиная с какой-то даты
        maxResults=100,
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    
    events = events_result.get('items', [])
    
    print(f"Found {len(events)} events")
    
    # Удаляем каждое событие
    for event in events:
        if event['summary'].startswith('Test Task'):  # удаляем только тестовые задачи
            try:
                calendar_service.events().delete(
                    calendarId='primary',
                    eventId=event['id']
                ).execute()
                print(f"Deleted event: {event['summary']}")
            except Exception as e:
                print(f"Error deleting event {event['id']}: {e}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(clean_calendar())