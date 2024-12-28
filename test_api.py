import requests
from datetime import datetime, timedelta, UTC

BASE_URL = "http://localhost:8000/tasks"

def test_create_and_get_task():
    task_data = {
        "title": "Test Task",
        "description": "Test Description",
        "deadline": (datetime.now(UTC) + timedelta(days=1)).isoformat()
    }

    # Create task
    response = requests.post(BASE_URL, json=task_data)
    print("\nStatus code:", response.status_code)
    print("Server response:", response.json())
    
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

def test_validation():
    # Тест 1: Пустой title (должен вернуть ошибку)
    invalid_task = {
        "title": "",  # Нарушает min_length=1
        "description": "Test Description"
    }
    response = requests.post(BASE_URL, json=invalid_task)
    print("\nTest 1 - Empty title:")
    print(f"Status code: {response.status_code}")  # Должен быть 422
    print(f"Response: {response.json()}")

    # Тест 2: Слишком длинный title (должен вернуть ошибку)
    invalid_task = {
        "title": "A" * 101,  # Нарушает max_length=100
        "description": "Test Description"
    }
    response = requests.post(BASE_URL, json=invalid_task)
    print("\nTest 2 - Too long title:")
    print(f"Status code: {response.status_code}")  # Должен быть 422
    print(f"Response: {response.json()}")

    # Тест 3: Некорректный формат даты
    invalid_task = {
        "title": "Test Task",
        "deadline": "not-a-date"  # Неверный формат datetime
    }
    response = requests.post(BASE_URL, json=invalid_task)
    print("\nTest 3 - Invalid date format:")
    print(f"Status code: {response.status_code}")  # Должен быть 422
    print(f"Response: {response.json()}")

    # Тест 4: Корректные данные (должно работать)
    valid_task = {
        "title": "Test Task",
        "description": "Test Description",
        "deadline": datetime.now(UTC).isoformat()
    }
    response = requests.post(BASE_URL, json=valid_task)
    print("\nTest 4 - Valid data:")
    print(f"Status code: {response.status_code}")  # Должен быть 200
    print(f"Response: {response.json()}")

if __name__ == "__main__":
    test_create_and_get_task()
    test_validation()