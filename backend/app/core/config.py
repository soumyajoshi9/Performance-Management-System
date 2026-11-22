from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
import os

class Settings(BaseSettings):
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    APP_NAME: str = "VYORA"
    APP_VERSION: str = "1.0.0-MVP"
    
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    ALLOWED_ORIGINS: str = "http://localhost:3000,http://127.0.0.1:3000"
    
    VYORA_DATABASE_URL: str = ""
    DATABASE_URL: str = "sqlite:///./vyora.db"
    DATABASE_TEST_URL: str = "sqlite:///./vyora_test.db"
    
    JWT_SECRET_KEY: str = "vyora-dev-secret-key-32-chars-long-secure-key"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    GEMINI_API_KEY: str = ""
    AI_MODEL_NAME: str = "gemini-1.5-pro"
    AI_TEMPERATURE: float = 0.1
    AI_TIMEOUT_SECONDS: int = 15
    
    LOG_LEVEL: str = "INFO"
    
    model_config = SettingsConfigDict(
        env_file=(".env", "../.env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

    @property
    def effective_database_url(self) -> str:
        # Prevent picking up unrelated ambient database URLs (e.g. hospital_db)
        if self.VYORA_DATABASE_URL:
            return self.VYORA_DATABASE_URL
        if "hospital_db" in self.DATABASE_URL or not (self.DATABASE_URL.startswith("postgresql") or self.DATABASE_URL.startswith("sqlite")):
            return "sqlite:///./vyora.db"
        return self.DATABASE_URL

    @property
    def cors_origins(self) -> List[str]:
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",") if origin.strip()]

settings = Settings()
