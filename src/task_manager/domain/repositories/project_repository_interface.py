from abc import ABC, abstractmethod
from typing import List, Optional
from src.task_manager.domain.entities.project import Project

class ProjectRepositoryInterface:
    @abstractmethod
    async def create_project(self, project: Project) -> Project:
        pass

    @abstractmethod
    async def get_project_by_id(self, project_id: int) -> Optional[Project]:
        pass

    @abstractmethod
    async def get_all_projects(self) -> List[Project]:
        pass

    @abstractmethod
    async def update_project(self, project_id: int, project: Project) -> Project:
        pass

    @abstractmethod
    async def delete_project(self, project_id: int) -> bool:
        pass

    