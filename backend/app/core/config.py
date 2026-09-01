from pydantic_settings import BaseSettings
from typing import List, Union
from pydantic import AnyHttpUrl, validator

class Settings(BaseSettings):
    PROJECT_NAME: str = "Think2Act"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = "development"
    
    # DB URL - defaults to local postgres or docker
    DATABASE_URL: str = "postgresql+asyncpg://think2act:think2act_password@localhost:5432/think2act_db"
    SYNC_DATABASE_URL: str = "postgresql://think2act:think2act_password@localhost:5432/think2act_db"
    
    # JWT & Auth
    JWT_SECRET: str = "think2act_super_secret_jwt_key_2026_change_in_prod"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 day

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://localhost:8000"
    ]

    class Config:
        case_sensitive = True
        env_file = ".env"
        extra = "allow"

settings = Settings()
