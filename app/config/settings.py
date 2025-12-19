import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    APP_NAME: str = "Placeholder API"
    DEBUG: bool = True
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./placeholder.db")
    
    class Config:
        env_file = ".env"


settings = Settings()