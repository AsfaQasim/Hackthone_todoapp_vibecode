"""Environment configuration management for the AI Chatbot with MCP application."""

from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Database settings
    @property
    def database_url(self) -> str:
        env_database_url = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:password@localhost/dbname")
        if not os.getenv("ENVIRONMENT") or os.getenv("ENVIRONMENT") == "development":
            # Check if it's the default PostgreSQL URL or the production Neon URL
            if "neon.tech" in env_database_url or "postgresql" in env_database_url:
                # Use absolute path to ensure consistency regardless of working directory
                import pathlib
                db_path = pathlib.Path(__file__).parent.parent.parent / "todo_app_local.db"
                return f"sqlite:///{db_path.as_posix()}"
            else:
                return env_database_url
        else:
            return env_database_url
    
    # JWT settings
    secret_key: str = os.getenv("BETTER_AUTH_SECRET", "your-secret-key-change-in-production")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440  # 24 hours instead of 30 minutes
    
    @property
    def jwt_secret(self) -> str:
        """Get JWT secret key."""
        return self.secret_key
    
    # OpenAI settings
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    
    # Application settings
    app_name: str = "AI Chatbot with MCP"
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"
    environment: str = os.getenv("ENVIRONMENT", "development")
    
    # API settings
    api_prefix: str = "/api"
    allowed_origins: str = os.getenv("ALLOWED_ORIGINS", "*")
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "allow"

# Create a single instance of settings
settings = Settings()