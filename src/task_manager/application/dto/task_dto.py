from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from src.task_manager.domain.value_objects.task_status import TaskStatus

class TaskDTO(BaseModel):
    """Базовый DTO для задач"""
    title: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.NEW
    deadline: Optional[datetime] = None
    project_id: Optional[int] = None

class CreateTaskDTO(TaskDTO):
    """DTO для создания задачи - наследует все поля от TaskDTO"""
    pass

class UpdateTaskDTO(TaskDTO):
    """DTO для обновления задачи - все поля опциональны"""
    title: Optional[str] = None
    status: Optional[TaskStatus] = None

class TaskResponseDTO(TaskDTO):
    """DTO для ответа - добавляет поля id и timestamps"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

    @classmethod
    def from_entity(cls, task):
        return cls(
            id=task.id,
            title=task.title,
            description=task.description,
            status=TaskStatus[task.status],
            deadline=task.deadline,
            project_id=task.project_id,
            created_at=task.created_at,
            updated_at=task.updated_at
        )