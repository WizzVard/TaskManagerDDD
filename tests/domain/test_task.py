import pytest
from datetime import datetime, timedelta
from src.task_manager.domain.entities.task import Task, InvalidStatusTransition
from src.task_manager.domain.value_objects.task_status import TaskStatus

def test_task_creation():
    task = Task(title="Test Task")
    assert task.title == "Test Task"
    assert task.status == TaskStatus.NEW.value

def test_invalid_status_transition():
    task = Task(title="Test Task")
    with pytest.raises(InvalidStatusTransition):
        task.change_status(TaskStatus.DONE) # We can't change status to DONE immediately

def test_valid_status_transition():
    task = Task(title="Test Task")
    task.status = TaskStatus.NEW.value
    task.change_status(TaskStatus.SCHEDULED)
    assert task.status == TaskStatus.SCHEDULED.value

def test_empty_title():
    with pytest.raises(ValueError):
        Task(title="")

def test_past_deadline():
    past_date = datetime.utcnow() - timedelta(days=1)
    with pytest.raises(ValueError):
        task = Task(title="Test Task")
        task.set_deadline(past_date)
