from datetime import datetime, UTC
from typing import Optional, Union
from src.task_manager.application.dto.task_dto import CreateTaskDTO
from src.task_manager.domain.value_objects.task_status import TaskStatus


class InvalidStatusTransition(Exception):
    """Exception raised for invalid status transition."""
    pass


class Task:
    def __init__(
        self,
        title: str,
        description: Optional[str] = None,
        status: Union[str, TaskStatus] = TaskStatus.NEW,
        deadline: Optional[datetime] = None,
        project_id: Optional[int] = None,
        color: Optional[str] = None,
        id: Optional[int] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        calendar_event_id: Optional[str] = None
    ):
        if not title:
            raise ValueError("Title cannot be empty")
        self.id = id
        self.title = title
        self.description = description
        self.status = status.value if isinstance(status, TaskStatus) else status
        self.deadline = deadline
        self.project_id = project_id
        self.color = color
        self.created_at = created_at or datetime.now(UTC)
        self.updated_at = updated_at
        self.calendar_event_id = calendar_event_id

    @classmethod
    def from_dto(cls, dto: CreateTaskDTO) -> "Task":
        return cls(
            title = dto.title,
            description = dto.description,
            status = dto.status,
            deadline = dto.deadline,
            project_id = dto.project_id,
            color = dto.color
        )

    def set_title(self, title: str):
        if not title:
            raise ValueError("Title cannot be empty")
        self.title = title

    def set_description(self, description: str):
        self.description = description

    def set_deadline(self, deadline: datetime):
        if deadline and deadline < datetime.now():
            raise ValueError("Deadline cannot be in the past")
        self.deadline = deadline

    def change_status(self, new_status: TaskStatus):
        if self._can_transition_to(new_status):
            self.status = new_status.value
        else:
            raise InvalidStatusTransition(f"Cannot transition from {self.status} to {new_status.value}")
        
    def _can_transition_to(self, new_status: TaskStatus) -> bool:
        try:
            current_status = TaskStatus(self.status)
            transitions = {
                TaskStatus.NEW: [TaskStatus.SCHEDULED, TaskStatus.CANCELED],
                TaskStatus.SCHEDULED: [TaskStatus.IN_PROGRESS, TaskStatus.CANCELED],
                TaskStatus.IN_PROGRESS: [TaskStatus.BLOCKED, TaskStatus.DONE],
                TaskStatus.BLOCKED: [TaskStatus.IN_PROGRESS, TaskStatus.CANCELED],
                TaskStatus.DONE: [],
                TaskStatus.CANCELED: [],
            }
            return new_status in transitions[current_status]
        except ValueError:
            return False

    def __repr__(self):
        return (f"Task(id={self.id}, title={self.title}, description={self.description}, status={self.status.value}, deadline={self.deadline}, project_id={self.project_id})")

if __name__ == "__main__":
    try:
        task = Task(id="1", title="Implement Task Management System", deadline=datetime(2024, 12, 31))
        print(task)
        task.change_status(TaskStatus.SCHEDULED)
        print(task)
        task.change_status(TaskStatus.IN_PROGRESS)
        print(task)
        task.change_status(TaskStatus.DONE)
        print(task)
    except (ValueError, InvalidStatusTransition) as e:
        print(f"Error: {e}")