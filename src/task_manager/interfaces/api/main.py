from fastapi import FastAPI
from .task_router import router

app = FastAPI(
    title="Task Management API",
    description="API for managing tasks and projects",
    docs_url="/docs" # URL for Swagger UI
)

app.include_router(router)