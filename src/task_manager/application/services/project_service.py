from src.task_manager.domain.entities.project import Project
from src.task_manager.domain.entities.task import Task
from src.task_manager.domain.repositories.project_repository_interface import ProjectRepositoryInterface
from src.task_manager.domain.repositories.calendar_repository_interface import CalendarRepositoryInterface
from src.task_manager.application.dto.project_dto import CreateProjectDTO
from src.task_manager.application.dto.project_dto import UpdateProjectDTO
from src.task_manager.domain.repositories.task_repository_interface import TaskRepositoryInterface
import asyncio
from typing import List, Dict, Tuple


class ProjectService:
    def __init__(self, 
                 project_repository: ProjectRepositoryInterface,
                 task_repository: TaskRepositoryInterface,
                 calendar_repository: CalendarRepositoryInterface):
        self.project_repository = project_repository
        self.task_repository = task_repository
        self.calendar_repository = calendar_repository

    async def create_project(self, data: CreateProjectDTO) -> Project:
        project = Project(
            name=data.name,
            description=data.description,
            color=data.color
        )
        return await self.project_repository.create_project(project)
    
    async def get_project(self, project_id: int) -> Project:
        project = await self.project_repository.get_project_by_id(project_id)
        if not project:
            raise ValueError("Project not found")
        return project
    
    async def get_all_projects_with_tasks(self) -> List[Tuple[Project, List[Task]]]:
        return await self.project_repository.get_all_projects_with_tasks()
    
    async def update_project(self, project_id: int, project_data: UpdateProjectDTO) -> Project:
        # Получаем существующий проект
        project = await self.project_repository.get_project_by_id(project_id)
        if not project:
            print(f"Project with id {project_id} not found")
            return
        
        if project_data.name:
            project.name = project_data.name
        if project_data.description:
            project.description = project_data.description
        if project_data.color:
            project.color = project_data.color

        # Сохраняем обновленный проект
        updated_project = await self.project_repository.update_project(project_id, project)

        # Если цвет проекта изменился, обновляем цвет всех связанных задач в календаре
        if project_data.color:
            tasks = await self.task_repository.get_tasks_by_project_id(project_id)
            update_futures = [
                self.calendar_repository.update_event(task, updated_project)
                for task in tasks
                if task.calendar_event_id
            ]

            if update_futures:
                await asyncio.gather(*update_futures)

        return updated_project

    async def delete_project(self, project_id: int) -> None:
        success = await self.project_repository.delete_project(project_id)
        if not success:
            raise ValueError("Failed to delete project")

