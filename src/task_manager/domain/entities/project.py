from typing import Optional, List
from datetime import datetime
from dataclasses import dataclass, field
from src.task_manager.domain.entities.task import Task
from src.task_manager.application.dto.project_dto import CreateProjectDTO
from datetime import UTC


@dataclass
class Project:
    id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    color: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None

    @classmethod
    def from_dto(cls, dto: CreateProjectDTO) -> "Project":
        return cls(
            name=dto.name,
            description=dto.description,
            color=dto.color
        )
    
    def set_name(self, name: str):
        if not name:
            raise ValueError("Name cannot be empty")
        self.name = name
        self.updated_at = datetime.now(UTC)

    def set_description(self, description: str):
        self.description = description
        self.updated_at = datetime.now(UTC)

    def set_color(self, color: str):
        self.color = color
        self.updated_at = datetime.now(UTC)

