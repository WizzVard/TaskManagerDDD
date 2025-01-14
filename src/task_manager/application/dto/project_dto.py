from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CreateProjectDTO(BaseModel):
    name: str
    description: Optional[str] = None
    color: Optional[str] = None

class UpdateProjectDTO(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    color: Optional[str] = None
    updated_at: Optional[datetime] = None

class ProjectResponseDTO(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    color: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True