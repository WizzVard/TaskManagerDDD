import pytest
from datetime import datetime, UTC


@pytest.mark.asyncio
async def test_create_project(project_repository, sample_project):
    created_project = await project_repository.create_project(sample_project)
    assert created_project.id is not None
    assert created_project.name == sample_project.name
    assert created_project.description == sample_project.description

@pytest.mark.asyncio
async def test_get_project_by_id(project_repository, sample_project):
    created_project = await project_repository.create_project(sample_project)
    retrieved_project = await project_repository.get_project_by_id(created_project.id)
    assert retrieved_project is not None
    assert retrieved_project.id == created_project.id
    assert retrieved_project.name == created_project.name
    assert retrieved_project.description == created_project.description
    assert retrieved_project.created_at is not None

@pytest.mark.asyncio
async def test_get_all_projects(project_repository, sample_project):
    created_project = await project_repository.create_project(sample_project)
    created_project2 = await project_repository.create_project(sample_project)
    retrieved_projects = await project_repository.get_all_projects()
    assert len(retrieved_projects) == 2
    assert created_project.id in [project.id for project in retrieved_projects]
    assert created_project2.id in [project.id for project in retrieved_projects]

@pytest.mark.asyncio
async def test_update_project(project_repository, sample_project):
    created_project = await project_repository.create_project(sample_project)
    created_project.name = "Updated Name"
    updated_project = await project_repository.update_project(created_project.id, created_project)
    assert updated_project.name == "Updated Name"

@pytest.mark.asyncio
async def test_delete_project(project_repository, sample_project):
    created_project = await project_repository.create_project(sample_project)
    result = await project_repository.delete_project(created_project.id)
    assert result is True
    deleted_project = await project_repository.get_project_by_id(created_project.id)
    assert deleted_project is None
