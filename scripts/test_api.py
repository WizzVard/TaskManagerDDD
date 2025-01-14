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
        "color": "#FFB878"  # Tangerine (colorId: 6)
    }
    response = requests.post(PROJECT_URL, json=project_data)
    print("\nCreate Project Status code:", response.status_code)
    project = response.json()
    project_id = project["id"]
    print(f"Created project with color: {project['color']}")
    
    # Создаем задачу в проекте
    task_data = {
        "title": "Test Task",
        "description": "Test Description",
        "deadline": (datetime.now(UTC) + timedelta(days=1)).isoformat(),
        "project_id": int(project_id)
    }

    # Create task
    response = requests.post(TASK_URL, json=task_data)
    print("\nCreate Task Status code:", response.status_code)
    created_task = response.json()
    print("Created task:", created_task)

    # # Create another task
    # response = requests.post(TASK_URL, json=task_data)
    # print("\nCreate Task Status code:", response.status_code)
    # created_task = response.json()
    # print("Created task:", created_task)
    # task_id = created_task['id']

    # # Update task
    # task_data_updated = {
    #     "title": "Test Task Updated",
    #     "description": "Test Description Updated",
    #     "project_id": project_id
    # }

    # response = requests.patch(f"{TASK_URL}/{task_id}", json=task_data_updated)
    # print("\nUpdate Status code:", response.status_code)
    # updated_task = response.json()
    # print("Updated task:", updated_task)

    # # project_id = 23

    # # Update project
    # project_data_updated = {
    #     "name": "Test Project Updated 2",
    #     "description": "Test Project Description Updated",
    #     # "color": "#FFB878"  # Tangerine (colorId: 6)
    #     "color": "#51B749"  # Basil (colorId: 10)
    # }

    # response = requests.patch(f"{PROJECT_URL}/{project_id}", json=project_data_updated)
    # print("\nUpdate Status code:", response.status_code)
    # updated_project = response.json()
    # print("Updated project:", updated_project)

    # Get all projects with tasks
    response = requests.get(f"{PROJECT_URL}/with-tasks")
    print("\nGet all projects with tasks Status code:", response.status_code)
    projects_with_tasks = response.json()
    print("Projects with tasks:", projects_with_tasks)


if __name__ == "__main__":
    test_task_manager()
