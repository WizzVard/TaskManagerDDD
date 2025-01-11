from src.task_manager.domain.entities.task import Task
from src.task_manager.infrastructure.repositories.task_repository import TaskRepository
from src.task_manager.infrastructure.repositories.google_calendar_repository import GoogleCalendarRepository
from src.task_manager.application.dto.task_dto import CreateTaskDTO, UpdateTaskDTO
from src.task_manager.domain.repositories.calendar_repository_interface import CalendarRepositoryInterface
from src.task_manager.domain.repositories.task_repository_interface import TaskRepositoryInterface
from src.task_manager.domain.entities.project import Project

class TaskService:
    def __init__(
        self, 
        task_repository: TaskRepositoryInterface,
        calendar_repository: CalendarRepositoryInterface
    ):
        self.task_repository = task_repository
        self.calendar_repository = calendar_repository

    async def create_task(self, data: CreateTaskDTO, project_id: str | None = None) -> Task:
        project = None
        if project_id:
            project = await self.project_repository.get_project_by_id(project_id)
        
        task = Task(
            title=data.title,
            description=data.description,
            deadline=data.deadline,
            project=project
        )

        # Создаем событие в календаре через репозиторий
        event_id = await self.calendar_repository.create_event(task)
        task.calendar_event_id = event_id
        
        # Сохраняем задачу через репозиторий
        return await self.task_repository.create_task(task)

    async def get_task(self, task_id: int) -> Task:
        return await self.task_repository.get_task_by_id(task_id)

    async def get_all_tasks(self) -> list[Task]:
        return await self.task_repository.get_all_tasks()

    async def update_task(self, task_id: int, data: UpdateTaskDTO) -> Task:
        existing_task = await self.get_task(task_id)
        if not existing_task:
            raise ValueError("Task not found")

        task = Task(
            id=task_id,
            title=data.title or existing_task.title,
            description=data.description or existing_task.description,
            status=data.status or existing_task.status,
            deadline=data.deadline or existing_task.deadline,
            project_id=data.project_id or existing_task.project_id,
            calendar_event_id=existing_task.calendar_event_id
        )

        await self.calendar_repository.update_event(task)
        
        return await self.task_repository.update_task(task_id, task)

    async def delete_task(self, task_id: int) -> bool:
        task = await self.get_task(task_id)
        if task:
            await self.calendar_repository.delete_event(task)
        return await self.task_repository.delete_task(task_id)

            
        