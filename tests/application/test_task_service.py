import pytest
from unittest.mock import Mock, AsyncMock
from src.task_manager.application.dto.task_dto import CreateTaskDTO, UpdateTaskDTO

@pytest.mark.asyncio
async def test_create_task(task_service, sample_task):
    task_dto = CreateTaskDTO(
        title=sample_task.title,
        description=sample_task.description,
        deadline=sample_task.deadline
    )
    created_task = await task_service.create_task(task_dto)
    assert created_task.id is not None
    assert created_task.title == task_dto.title

@pytest.mark.asyncio
async def test_update_task(task_service, sample_task):
    # Создаем задачу
    created_task = await task_service.create_task(CreateTaskDTO(
        title=sample_task.title,
        description=sample_task.description
    ))
    
    # Обновляем задачу
    update_dto = UpdateTaskDTO(title="Updated Title")
    updated_task = await task_service.update_task(created_task.id, update_dto)
    assert updated_task.title == "Updated Title"

@pytest.mark.asyncio
async def test_delete_task(task_service, sample_task):
    # Создаем задачу
    task_dto = CreateTaskDTO(
        title=sample_task.title,
        description=sample_task.description
    )
    created_task = await task_service.create_task(task_dto)
    
    # Удаляем задачу
    result = await task_service.delete_task(created_task.id)
    assert result is True 