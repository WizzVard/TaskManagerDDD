from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_HOST: str = "localhost"
    DB_PORT: str = "5432"
    DB_NAME: str = "taskmanager"
    DB_USER: str = "postgres"
    DB_PASS: str = "22032004"
    
    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
