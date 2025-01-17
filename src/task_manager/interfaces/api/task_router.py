from fastapi import APIRouter, Depends, HTTPException
from typing import List

from src.task_manager.application.dto.task_dto import CreateTaskDTO, UpdateTaskDTO, TaskResponseDTO
from src.task_manager.application.services.task_service import TaskService
from src.core.dependencies import get_task_service
from src.task_manager.application.services.project_service import ProjectService
from src.task_manager.application.dto.project_dto import CreateProjectDTO, UpdateProjectDTO, ProjectResponseDTO
from src.core.dependencies import get_project_service

import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/tasks", 
    tags=["tasks"]
)

@router.post("", response_model=TaskResponseDTO)
async def create_task(
    task_dto: CreateTaskDTO,
    task_service: TaskService = Depends(get_task_service)
) -> TaskResponseDTO:
    """Create a new task"""
    try:
        task = await task_service.create_task(task_dto)
        return TaskResponseDTO.model_validate(task)
    except Exception as e:
        logger.error(f"Error creating task: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/projects/{project_id}/tasks")
async def get_tasks_by_project(
    project_id: int,
    task_service: TaskService = Depends(get_task_service)
) -> List[TaskResponseDTO]:
    tasks = await task_service.get_tasks_by_project(project_id)
    return [TaskResponseDTO.from_entity(task) for task in tasks]


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
    try:
        task = await task_service.update_task(task_id, task_dto)
        return TaskResponseDTO.model_validate(task)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{task_id}", status_code=204)
async def delete_task(
    task_id: int,
    task_service: TaskService = Depends(get_task_service)
) -> None:
    try: 
        await task_service.delete_task(task_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
