from abc import ABC, abstractmethod
from typing import List, Optional
from src.task_manager.domain.entities.task import Task

class TaskRepositoryInterface(ABC):
    @abstractmethod
    async def create_task(self, task: Task) -> Task:
        """Create a new task"""
        pass

    @abstractmethod
    async def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """Get task by ID"""
        pass

    @abstractmethod
    async def get_all_tasks(self) -> List[Task]:
        """Get all tasks"""
        pass

    @abstractmethod
    async def update_task(self, task_id: int, task: Task) -> Optional[Task]:
        """Update existing task"""
        pass

    @abstractmethod
    async def delete_task(self, task_id: int) -> bool:
        """Delete task by ID"""
        pass
