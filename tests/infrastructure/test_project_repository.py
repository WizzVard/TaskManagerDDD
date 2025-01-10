import pytest
from datetime import datetime, UTC


@pytest.mark.asyncio
async def test_create_project(project_repository, sample_project):

    # Act
    created_project = await project_repository.create_project(sample_project)

    # Assert
    assert created_project.id is not None
    assert created_project.name == sample_project.name
    assert created_project.description == sample_project.description


@pytest.mark.asyncio
async def test_get_project_by_id(project_repository):
    pass