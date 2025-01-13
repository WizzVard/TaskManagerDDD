from src.task_manager.domain.entities.project import Project
from src.task_manager.domain.repositories.project_repository_interface import ProjectRepositoryInterface
from src.task_manager.domain.repositories.calendar_repository_interface import CalendarRepositoryInterface
from src.task_manager.application.dto.project_dto import CreateProjectDTO

class ProjectService:
    def __init__(self, 
                project_repository: ProjectRepositoryInterface,
                calendar_repository: CalendarRepositoryInterface):
        self.project_repository = project_repository
        self.calendar_repository = calendar_repository

    async def create_project(self, data: CreateProjectDTO) -> Project:
        project = Project(
            name=data.name,
            description=data.description,
            color=data.color
        )
        return await self.project_repository.create_project(project)
    
    async def get_project(self, project_id: int) -> Project:
        return await self.project_repository.get_project_by_id(project_id)
    
    # async def update_project(self, project_id: int, data: UpdateProjectDTO) -> Project:
        # existing_project = await self.get_project(project_id)

