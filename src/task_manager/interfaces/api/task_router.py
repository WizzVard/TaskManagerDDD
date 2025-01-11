from fastapi import APIRouter, Depends, HTTPException
from typing import List

from src.task_manager.application.dto.task_dto import CreateTaskDTO, UpdateTaskDTO, TaskResponseDTO
from src.task_manager.application.services.task_service import TaskService
from src.core.dependencies import get_task_service
from src.task_manager.application.services.project_service import ProjectService
from src.task_manager.application.dto.project_dto import CreateProjectDTO, UpdateProjectDTO, ProjectResponseDTO
from src.core.dependencies import get_project_service


router = APIRouter(
    prefix="/tasks", 
    tags=["tasks"]
)

@router.post("/projects")
async def create_project(
    project_dto: CreateProjectDTO,
    project_service: ProjectService = Depends(get_project_service)
) -> ProjectResponseDTO:
    project = await project_service.create_project(project_dto)
    return ProjectResponseDTO.model_validate(project)

@router.post("", response_model=TaskResponseDTO)
async def create_task(
    task_dto: CreateTaskDTO,
    task_service: TaskService = Depends(get_task_service)
) -> TaskResponseDTO:
    "Create a new task"
    task = await task_service.create_task(task_dto)
    return TaskResponseDTO.model_validate(task)

@router.get("/{task_id}", response_model=TaskResponseDTO)
async def get_task(
    task_id: int,
    task_service: TaskService = Depends(get_task_service)
) -> TaskResponseDTO:
    "Get a task by its ID"
    task = await task_service.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskResponseDTO.model_validate(task)


@router.get("", response_model=List[TaskResponseDTO])
async def get_tasks(
    task_service: TaskService = Depends(get_task_service)
) -> List[TaskResponseDTO]:
    "Get all tasks"
    try:
        tasks = await task_service.get_all_tasks()
        print(f"Retrieved {len(tasks)} tasks from service")
        result = [TaskResponseDTO.from_entity(task) for task in tasks]
        print(f"Converted to {len(result)} DTOs")
        return result
    except Exception as e:
        print(f"Error in get_tasks endpoint: {e}")
        raise

@router.patch("/{task_id}", response_model=TaskResponseDTO)
async def update_task(
    task_id: int,
    task_dto:  UpdateTaskDTO,
    task_service: TaskService = Depends(get_task_service)
) -> TaskResponseDTO:
    "Update a task by its ID"
    task = await task_service.update_task(task_id, task_dto)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskResponseDTO.model_validate(task)

@router.delete("/{task_id}", status_code=204)
async def delete_task(
    task_id: int,
    task_service: TaskService = Depends(get_task_service)
) -> None:
    "Delete a task by its ID"
    success = await task_service.delete_task(task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
