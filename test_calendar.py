from src.task_manager.infrastructure.external_services.google_calendar_client import GoogleCalendarClient
from src.task_manager.domain.entities.task import Task
from datetime import datetime, timedelta, UTC
import asyncio

async def test_calendar_integration():
    # Create a calendar client
    calendar_client = GoogleCalendarClient()
    
    # Create a task
    task = Task(
        title="Test Calendar Integration",
        description="Testing Google Calendar integration",
        deadline=datetime.now(UTC) + timedelta(days=1)
    )

    try:
        # Create an event
        print("Creating event...")
        event_id = await calendar_client.create_event(task)
        print(f"Event created with ID: {event_id}")
        
        # Save event_id to task
        task.calendar_event_id = event_id
        
        # Update task
        print("\nUpdating event...")
        task.title = "Updated Test Task"
        await calendar_client.update_event(task)
        print("Event updated")
        
        # Delete event
        print("\nDeleting event...")
        await calendar_client.delete_event(task)
        print("Event deleted")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_calendar_integration())