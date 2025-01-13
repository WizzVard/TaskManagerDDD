from datetime import datetime, timedelta
from src.task_manager.domain.repositories.calendar_repository_interface import CalendarRepositoryInterface
from src.task_manager.domain.entities.task import Task
from src.task_manager.infrastructure.external.google_calendar_api import GoogleCalendarAPI
import logging

logger = logging.getLogger(__name__)

class GoogleCalendarRepository(CalendarRepositoryInterface):
    def __init__(self):
        self.calendar_api = GoogleCalendarAPI()

    def _get_color_id(self, hex_color: str) -> str:
        color_map = {
            '#AC725E': '1',  # Коричневый
            '#D06B64': '2',  # Красный
            '#F83A22': '3',  # Оранжевый
            '#FA573C': '4',  # Оранжево-красный
            '#FF7537': '5',  # Желтый
            '#42D692': '6',  # Зеленый
            '#92E1C0': '7',  # Бирюзовый
            '#9FE1E7': '8',  # Голубой
            '#9FC6E7': '9',  # Синий
            '#B99AFF': '10', # Фиолетовый
            '#C2C2C2': '11'  # Серый
        }
        logger.info(f"Converting hex color {hex_color} to Google Calendar color ID")
        color_id = min(color_map.items(), key=lambda x: self._color_distance(hex_color, x[0]))[1]
        logger.info(f"Selected color ID: {color_id}")
        return color_id
    
    def _color_distance(self, hex1: str, hex2: str) -> float:
        # Вычисляем "расстояние" между двумя hex цветами
        r1, g1, b1 = int(hex1[1:3], 16), int(hex1[3:5], 16), int(hex1[5:7], 16)
        r2, g2, b2 = int(hex2[1:3], 16), int(hex2[3:5], 16), int(hex2[5:7], 16)
        return ((r1-r2)**2 + (g1-g2)**2 + (b1-b2)**2) ** 0.5

    async def create_event(self, task: Task, project = None) -> str:
        if not task.deadline:
            raise ValueError("Task must have a deadline to create calendar event")

        # Используем цвет из проекта или из задачи
        color = project.color if project and project.color else task.color

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
            'colorId': self._get_color_id(color) if color else '1'  # Default blue
        }

        try:
            result = self.calendar_api.create_calendar_event(event_data)
            return result['id']
        except Exception as e:
            print(f'Error creating event: {e}')
            raise

    async def update_event(self, task: Task, project = None) -> None:
        if not task.calendar_event_id:
            return

        # Используем цвет из проекта или из задачи, как в create_event
        color = project.color if project and project.color else task.color

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
            },
            'colorId': self._get_color_id(color) if color else '1'  # Default blue
        }

        try:
            self.calendar_api.update_calendar_event(task.calendar_event_id, event_data)
        except Exception as e:
            print(f'Error updating event: {e}')
            raise

    async def delete_event(self, task: Task) -> None:
        if not task.calendar_event_id:
            logger.info(f"No calendar_event_id for task {task.id}")
            return

        try:
            logger.info(f"Deleting calendar event {task.calendar_event_id} for task {task.id}")
            self.calendar_api.delete_calendar_event(task.calendar_event_id)
            logger.info(f"Successfully deleted calendar event {task.calendar_event_id}")
        except Exception as e:
            logger.error(f"Error deleting event {task.calendar_event_id}: {e}")
            raise 
