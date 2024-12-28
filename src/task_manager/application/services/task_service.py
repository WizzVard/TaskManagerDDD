from src.task_manager.domain.entities.task import Task
from src.task_manager.infrastructure.repositories.task_repository import TaskRepository
from src.task_manager.infrastructure.google_calendar_client import GoogleCalendarClient
from src.task_manager.application.dto.task_dto import CreateTaskDTO, UpdateTaskDTO

class TaskService:
    def __init__(self, task_repository: TaskRepository, calendar_client: GoogleCalendarClient):
        self.task_repository = task_repository
        self.calendar_client = calendar_client

    async def create_task(self, data: CreateTaskDTO) -> Task:
        task = Task(
            title=data.title,
            description=data.description,
            status=data.status,
            deadline=data.deadline,
            project_id=data.project_id
        )
        created_task = await self.task_repository.create_task(task)
        await self.calendar_client.create_event(created_task)
        return created_task

    async def get_task(self, task_id: int) -> Task:
        return await self.task_repository.get_task_by_id(task_id)

    async def get_all_tasks(self) -> list[Task]:
        return await self.task_repository.get_all_tasks()

    async def update_task(self, task_id: int, data: UpdateTaskDTO) -> Task:
        task = Task(
            id=task_id,
            title=data.title,
            description=data.description,
            status=data.status,
            deadline=data.deadline,
            project_id=data.project_id
        )
        updated_task = await self.task_repository.update_task(task_id, task)
        await self.calendar_client.update_event(updated_task)
        return updated_task

    async def delete_task(self, task_id: int) -> bool:
        task = await self.get_task(task_id)
        if task:
            await self.calendar_client.delete_event(task)
        return await self.task_repository.delete_task(task_id)

            
        