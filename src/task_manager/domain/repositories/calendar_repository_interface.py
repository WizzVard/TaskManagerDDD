from abc import ABC, abstractmethod
from src.task_manager.domain.entities.task import Task
from src.task_manager.domain.entities.project import Project

class CalendarRepositoryInterface(ABC):
    @abstractmethod
    async def create_event(self, task: Task, project: Project = None) -> str:
        """Create calendar event for task and return event_id"""
        pass

    @abstractmethod
    async def update_event(self, task: Task) -> None:
        """Update calendar event for task"""
        pass

    @abstractmethod
    async def delete_event(self, task: Task) -> None:
        """Delete calendar event for task"""
        pass 