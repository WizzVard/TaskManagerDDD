from typing import Optional, List
from datetime import datetime
from dataclasses import dataclass, field
from src.task_manager.domain.entities.task import Task


@dataclass
class Project:
    id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    color: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None
    # tasks: List[Task] = None

    def add_task(self, task: 'Task'):
        if not self.tasks:
            self.tasks = []
        if len(self.tasks) >= 100: # Бизнес правило
            raise ValueError("Project cannot have more than 100 tasks")
        self.tasks.append(task)
