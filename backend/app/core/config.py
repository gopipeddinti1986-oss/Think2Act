from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):
    PROJECT_NAME: str = "Think2Act"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = "development"
    
    # Defaults to local SQLite if PostgreSQL is not running or specified
    DATABASE_URL: str = "sqlite+aiosqlite:///./think2act.db"
    
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

    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=".env",
        extra="allow"
    )

settings = Settings()
