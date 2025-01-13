import requests
from datetime import datetime, timedelta, UTC


BASE_URL = "http://localhost:8000"
TASK_URL = f"{BASE_URL}/tasks"
PROJECT_URL = f"{BASE_URL}/tasks/projects"


def test_task_manager():
    # Создаем проект
    project_data = {
        "name": "Test Project",
        "description": "Test Project Description",
        "color": "#FF7537"
    }
    response = requests.post(PROJECT_URL, json=project_data)
    print("\nCreate Project Status code:", response.status_code)
    project = response.json()
    project_id = project["id"]
    
    # Создаем задачу в проекте
    task_data = {
        "title": "Test Task",
        "description": "Test Description",
        "deadline": (datetime.now(UTC) + timedelta(days=1)).isoformat(),
        "project_id": project_id
    }

    # Create task
    response = requests.post(TASK_URL, json=task_data)
    print("\nCreate Task Status code:", response.status_code)
    print("Server response:", response.json())

    created_task = response.json()
    task_id = created_task['id']
    print("Created task ID:", task_id)

    task_data_updated = {
        "title": "Test Task Updated",
        "description": "Test Description Updated"
    }

    # Исправленные URL для операций с задачами
    response = requests.patch(f"{TASK_URL}/{task_id}", json=task_data_updated)
    print("\nUpdate Status code:", response.status_code)

    # Get all tasks
    response = requests.get(TASK_URL)
    tasks = response.json()
    print("\nGET Status code:", response.status_code)
    print("Task list:")
    for task in tasks:
        print(f"ID: {task['id']}")
        print(f"Title: {task['title']}")
        print(f"Description: {task['description']}")
        print(f"Status: {task['status']}")
        print(f"Created at: {task['created_at']}")
        print("---")

    # Delete task
    # response = requests.delete(f"{TASK_URL}/{task_id}")
    # print("\nDelete Status code:", response.status_code)


if __name__ == "__main__":
    test_task_manager()
