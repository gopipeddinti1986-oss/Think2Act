from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Optional
from pydantic import model_validator

class Settings(BaseSettings):
    PROJECT_NAME: str = "Think2Act"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = "development"
    
    # Defaults to local SQLite if PostgreSQL is not running or specified
    DATABASE_URL: str = "sqlite+aiosqlite:///./think2act.db"
    
    # JWT & Security
    JWT_SECRET: str = "think2act_dev_secret_key_2026_local_only"
    SECRET_KEY: Optional[str] = None
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 day
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    @model_validator(mode="after")
    def sync_secrets(self) -> "Settings":
        if self.SECRET_KEY and self.JWT_SECRET == "think2act_dev_secret_key_2026_local_only":
            self.JWT_SECRET = self.SECRET_KEY
        if self.ENVIRONMENT == "production" and self.JWT_SECRET == "think2act_dev_secret_key_2026_local_only":
            raise ValueError("JWT_SECRET must be explicitly set to a secure key when ENVIRONMENT is 'production'.")
        return self

    # Redis Cache & Queue
    REDIS_URL: Optional[str] = "redis://localhost:6379/0"

    # AI Provider Abstraction
    AI_PROVIDER: str = "mock"  # Options: mock, groq, openai, gemini
    AI_API_KEY: Optional[str] = None
    AI_MODEL: Optional[str] = None

    # Storage for Uploaded Resumes and Documents
    STORAGE_ENDPOINT: Optional[str] = None
    STORAGE_BUCKET: str = "think2act-documents"
    STORAGE_ACCESS_KEY: Optional[str] = None
    STORAGE_SECRET_KEY: Optional[str] = None

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://localhost:8000"
    ]

    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=(".env", "../.env"),
        extra="allow"
    )

settings = Settings()

