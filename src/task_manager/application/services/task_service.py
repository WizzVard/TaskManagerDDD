from src.task_manager.domain.entities.task import Task
from src.task_manager.application.dto.task_dto import CreateTaskDTO, UpdateTaskDTO
from src.task_manager.domain.repositories.calendar_repository_interface import CalendarRepositoryInterface
from src.task_manager.domain.repositories.task_repository_interface import TaskRepositoryInterface
from src.task_manager.domain.repositories.project_repository_interface import ProjectRepositoryInterface
from src.core.exceptions import TaskCreationException
from fastapi import HTTPException
from typing import List


class TaskService:
    def __init__(
        self, 
        task_repository: TaskRepositoryInterface,
        calendar_repository: CalendarRepositoryInterface,
        project_repository: ProjectRepositoryInterface
    ):
        self.task_repository = task_repository
        self.calendar_repository = calendar_repository
        self.project_repository = project_repository

    async def get_task(self, task_id: int) -> Task:
        return await self.task_repository.get_task_by_id(task_id)

    async def get_all_tasks(self) -> list[Task]:
        return await self.task_repository.get_all_tasks()
    
    async def get_tasks_by_project(self, project_id: int) -> List[Task]:
        return await self.task_repository.get_tasks_by_project(project_id)
    
    async def create_task(self, data: CreateTaskDTO) -> Task:
        task = None
        calendar_event_id = None
        try:
            # Fase 1: Create task in db without calendar_event_id
            task = Task.from_dto(data)
            task = await self.task_repository.create_task(task)

            # Fase 2: Create calendar event
            if task.deadline:
                project = None
                if task.project_id:
                    project = await self.project_repository.get_project_by_id(task.project_id)

                calendar_event_id = await self.calendar_repository.create_event(task, project)

                # Fase 3: Update task with calendar_event_id
                task.calendar_event_id = calendar_event_id
                task = await self.task_repository.update_task(task.id, task)

            return task

        except Exception as e:
            if calendar_event_id:
                await self.calendar_repository.delete_event(task)
            if task and task.id:
                await self.task_repository.delete_task(task.id)
            raise TaskCreationException(f"Failed to create task: {str(e)}")

    async def update_task(self, task_id: int, data: UpdateTaskDTO) -> Task:
        existing_task = await self.get_task(task_id)
        if not existing_task:
            raise ValueError("Task not found")

        project = None
        project_id = data.project_id or existing_task.project_id
        if project_id:
            project = await self.project_repository.get_project_by_id(project_id)

        task = Task(
            id=task_id,
            title=data.title or existing_task.title,
            description=data.description or existing_task.description,
            status=data.status or existing_task.status,
            deadline=data.deadline or existing_task.deadline,
            project_id=project_id,
            color=project.color if project else None,
            calendar_event_id=existing_task.calendar_event_id
        )

        if task.deadline:
            if task.calendar_event_id:
                await self.calendar_repository.update_event(task, project)
            else:
                event_id = await self.calendar_repository.create_event(task, project)
                task.calendar_event_id = event_id
        elif task.calendar_event_id:
            await self.calendar_repository.delete_event(task)
            task.calendar_event_id = None
        
        return await self.task_repository.update_task(task_id, task)


    async def delete_task(self, task_id: int) -> None:
        task = await self.task_repository.get_task_by_id(task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
                
        if task.calendar_event_id:
            try:
                await self.calendar_repository.delete_event(task)
            except Exception as e:
                raise
        
        success = await self.task_repository.delete_task(task_id)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to delete task")
    
    async def delete_all_tasks(self) -> None:
        tasks = await self.task_repository.get_all_tasks()
        for task in tasks:
            if task.calendar_event_id:
                await self.calendar_repository.delete_event(task)
        return await self.task_repository.delete_all_tasks()


            
        