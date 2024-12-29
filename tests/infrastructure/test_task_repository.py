import pytest
from datetime import datetime
from src.task_manager.domain.entities.task import Task

@pytest.mark.asyncio
async def test_create_task(task_repository, sample_task):
    created_task = await task_repository.create_task(sample_task)
    assert created_task.id is not None
    assert created_task.title == sample_task.title

@pytest.mark.asyncio
async def test_get_task_by_id(task_repository, sample_task):
    created_task = await task_repository.create_task(sample_task)
    retrieved_task = await task_repository.get_task_by_id(created_task.id)
    assert retrieved_task is not None
    assert retrieved_task.id == created_task.id
    assert retrieved_task.title == created_task.title

@pytest.mark.asyncio
async def test_update_task(task_repository, sample_task):
    created_task = await task_repository.create_task(sample_task)
    created_task.title = "Updated Title"
    updated_task = await task_repository.update_task(created_task.id, created_task)
    assert updated_task.title == "Updated Title"

@pytest.mark.asyncio
async def test_delete_task(task_repository, sample_task):
    created_task = await task_repository.create_task(sample_task)
    result = await task_repository.delete_task(created_task.id)
    assert result is True
    deleted_task = await task_repository.get_task_by_id(created_task.id)
    assert deleted_task is None 