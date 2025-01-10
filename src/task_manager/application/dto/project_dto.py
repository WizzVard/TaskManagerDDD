from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ProjectDTO(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None

class ProjectResponseDTO(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    task_count: int
    created_at: datetime
    updated_at: Optional[datetime] = None