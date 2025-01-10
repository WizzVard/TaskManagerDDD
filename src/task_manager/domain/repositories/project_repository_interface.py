from abc import ABC, abstractmethod
from typing import List, Optional
from src.task_manager.domain.entities.project import Project

class ProjectRepositoryInterface:
    @abstractmethod
    async def create_project(self, project: Project) -> Project:
        pass