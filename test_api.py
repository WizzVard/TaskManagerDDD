import requests
from datetime import datetime, timedelta, UTC

BASE_URL = "http://localhost:8000/tasks"

def test_task_manager():
    task_data = {
        "title": "Test Task",
        "description": "Test Description",
        "deadline": (datetime.now(UTC) + timedelta(days=1)).isoformat()
    }

    # Create task
    response = requests.post(BASE_URL, json=task_data)
    print("\nStatus code:", response.status_code)
    print("Server response:", response.json())

    task_data_updated = {
        "title": "Test Task Updated",
        "description": "Test Description Updated"
    }

    response = requests.delete(BASE_URL + "/16")
    print("\nStatus code:", response.status_code)
    
    response = requests.patch(BASE_URL + "/20", json=task_data_updated)
    print("\nStatus code:", response.status_code)
    
    # Get all tasks
    response = requests.get(BASE_URL)
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


if __name__ == "__main__":
    test_task_manager()