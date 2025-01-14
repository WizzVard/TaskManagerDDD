from fastapi import FastAPI
from .task_router import router as task_router
from .project_router import router as project_router

app = FastAPI(
    title="Task Management API",
    description="API for managing tasks and projects",
    docs_url="/docs"
)

app.include_router(task_router)
app.include_router(project_router)