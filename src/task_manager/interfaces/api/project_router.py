from fastapi import APIRouter, Depends
from src.task_manager.application.services.project_service import ProjectService
from src.task_manager.application.dto.project_dto import CreateProjectDTO, ProjectResponseDTO, UpdateProjectDTO
from src.core.dependencies import get_project_service
from fastapi import HTTPException
from typing import List, Dict, Tuple

router = APIRouter(
    prefix="/tasks/projects",
    tags=["projects"]
)

@router.post("", response_model=ProjectResponseDTO)
async def create_project(
    project_dto: CreateProjectDTO,
    project_service: ProjectService = Depends(get_project_service)
) -> ProjectResponseDTO:
    """Create a new project"""
    project = await project_service.create_project(project_dto)
    return ProjectResponseDTO.model_validate(project)

@router.patch("/{project_id}")
async def update_project(
    project_id: int,
    project_dto: UpdateProjectDTO,
    project_service: ProjectService = Depends(get_project_service)
) -> ProjectResponseDTO:
    try:
        return await project_service.update_project(project_id, project_dto)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
        
@router.delete("/{project_id}", status_code=204)
async def delete_project(
    project_id: int,
    project_service: ProjectService = Depends(get_project_service)
) -> None:
    try:
        await project_service.delete_project(project_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.get("/with-tasks")
async def get_all_projects_with_tasks(
    project_service: ProjectService = Depends(get_project_service)
) -> List[Dict]:
    projects_with_tasks = await project_service.get_all_projects_with_tasks()

    return [
        {
            "project": {
                "id": project.id,
                "name": project.name,
                "description": project.description,
                "color": project.color,
                "created_at": project.created_at,
                "updated_at": project.updated_at
            },
            "tasks": [
                {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "status": task.status,
                    "deadline": task.deadline,
                    "project_id": task.project_id,
                    "created_at": task.created_at,
                    "updated_at": task.updated_at
                }
                for task in tasks
            ]
        }
        for project, tasks in projects_with_tasks
    ]