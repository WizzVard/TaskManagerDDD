from datetime import datetime, timedelta
from src.task_manager.domain.repositories.calendar_repository_interface import CalendarRepositoryInterface
from src.task_manager.domain.entities.task import Task
from src.task_manager.infrastructure.external.google_calendar_api import GoogleCalendarAPI

class GoogleCalendarRepository(CalendarRepositoryInterface):
    def __init__(self):
        self.calendar_api = GoogleCalendarAPI()

    async def create_event(self, task: Task, project = None) -> dict:
        description = task.description or ""
        if project:
            description = f"Project: {project.name}\n\n{description}"
        
        event_data = {
            'summary': task.title,
            'description': description,
            'start': {
                'dateTime': task.deadline.isoformat() if task.deadline else 
                (datetime.now() + timedelta(days=1)).isoformat(),
                'timeZone': 'UTC',
            },
            'end': {
                'dateTime': (task.deadline + timedelta(hours=1)).isoformat() if task.deadline else 
                (datetime.now() + timedelta(days=1, hours=1)).isoformat(),
                'timeZone': 'UTC',
            },
            'reminders': {
                'useDefault': True
            },
            'extendedProperties': {
                'private': {
                    'taskId': str(task.id),
                    'projectId': str(project.id) if project else None
                }
            }
        }

        try:
            result = self.calendar_api.create_calendar_event(event_data)
            return result['id']
        except Exception as e:
            print(f'Error creating event: {e}')
            raise

    async def update_event(self, task: Task) -> None:
        if not task.calendar_event_id:
            return

        event_data = {
            'summary': task.title,
            'description': task.description,
            'start': {
                'dateTime': task.deadline.isoformat(),
                'timeZone': 'UTC'
            },
            'end': {
                'dateTime': (task.deadline + timedelta(hours=1)).isoformat(),
                'timeZone': 'UTC'
            }
        }

        try:
            self.calendar_api.update_calendar_event(task.calendar_event_id, event_data)
        except Exception as e:
            print(f'Error updating event: {e}')
            raise

    async def delete_event(self, task: Task) -> None:
        if not task.calendar_event_id:
            return

        try:
            self.calendar_api.delete_calendar_event(task.calendar_event_id)
        except Exception as e:
            print(f'Error deleting event: {e}')
            raise 