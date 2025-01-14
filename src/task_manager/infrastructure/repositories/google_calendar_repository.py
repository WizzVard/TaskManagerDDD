from datetime import datetime, timedelta
from src.task_manager.domain.repositories.calendar_repository_interface import CalendarRepositoryInterface
from src.task_manager.domain.entities.task import Task
from src.task_manager.domain.entities.project import Project
from src.task_manager.infrastructure.external.google_calendar_api import GoogleCalendarAPI


class GoogleCalendarRepository(CalendarRepositoryInterface):
    def __init__(self):
        self.calendar_api = GoogleCalendarAPI()
        self.color_map = {
            '#A4BDFC': '1',  # Lavender
            '#7AE7BF': '2',  # Sage
            '#DBADFF': '3',  # Grape
            '#FF887C': '4',  # Flamingo
            '#FBD75B': '5',  # Banana
            '#FFB878': '6',  # Tangerine
            '#46D6DB': '7',  # Peacock
            '#E1E1E1': '8',  # Gray
            '#5484ED': '9',  # Blueberry
            '#51B749': '10', # Basil
            '#DC2127': '11'  # Tomato
        }

    def _get_color_id(self, hex_color: str) -> str:
        print(f"\nGetting color ID for: {hex_color}")
        color_id = self.color_map.get(hex_color, '1')  # Default to Lavender if color not found
        print(f"Color ID: {color_id}")
        return color_id

    async def create_event(self, task: Task, project = None) -> str:
        if not task.deadline:
            raise ValueError("Task must have a deadline to create calendar event")

        color = project.color if project and project.color else task.color
        print(f"\nCreating event with color: {color}")

        event_data = {
            'summary': task.title,
            'description': task.description,
            'start': {
                'dateTime': task.deadline.isoformat(),
                'timeZone': 'UTC',
            },
            'end': {
                'dateTime': (task.deadline + timedelta(hours=1)).isoformat(),
                'timeZone': 'UTC',
            },
            'colorId': self._get_color_id(color)
        }
        print(f"Event data: {event_data}")

        try:
            result = self.calendar_api.create_calendar_event(event_data)
            return result['id']
        except Exception as e:
            print(f'Error creating event: {e}')
            raise

    async def update_event(self, task: Task, project: Project) -> str:
        print(f"\nUpdating event for task {task.id} with color: {project.color}")
        event = {
            'summary': task.title,
            'description': task.description,
            'colorId': self._get_color_id(project.color),
            'start': {
                'dateTime': task.deadline.isoformat() if task.deadline else None,
                'timeZone': 'UTC',
            },
            'end': {
                'dateTime': task.deadline.isoformat() if task.deadline else None,
                'timeZone': 'UTC',
            }
        }

        try:
            self.calendar_api.update_calendar_event(task.calendar_event_id, event)
        except Exception as e:
            print(f'Error updating event: {e}')
            raise

    async def delete_event(self, task: Task) -> None:
        if not task.calendar_event_id:
            print(f"No calendar_event_id for task {task.id}")
            return

        try:
            print(f"Deleting calendar event {task.calendar_event_id} for task {task.id}")
            self.calendar_api.delete_calendar_event(task.calendar_event_id)
            print(f"Successfully deleted calendar event {task.calendar_event_id}")
        except Exception as e:
            print(f"Error deleting event {task.calendar_event_id}: {e}")
            raise 
