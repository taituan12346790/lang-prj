# config.py - Configuration Management with Validation
from pydantic import Field, field_validator, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Literal
from loguru import logger


class Settings(BaseSettings):
    """Application Settings - Development Safe, Production Ready"""

    # ==================== DATABASE ====================
    DATABASE_URL: str = Field(
        ...,
        min_length=1,
        description="PostgreSQL connection string"
    )
    DB_ECHO: bool = Field(
        False,
        description="Echo SQL queries in logs (dev only)"
    )

    # ==================== SECURITY ====================
    SECRET_KEY: str = Field(
        ...,
        min_length=32,
        description="JWT signing key (minimum 32 characters)"
    )
    ALGORITHM: str = Field(
        "HS256",
        description="JWT algorithm"
    )
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        10080,  # 7 days
        ge=1,
        description="JWT token expiration in minutes"
    )

    # ==================== LLM ====================
    GROQ_API_KEY: str = Field(
        ...,
        min_length=1,
        description="Groq API key for LLM"
    )
    LLM_MODEL: str = Field(
        "openai/gpt-oss-120b",
        description="LLM model name"
    )
    LLM_TIMEOUT: int = Field(
        60,
        ge=10,
        description="LLM request timeout in seconds"
    )

    # ==================== GOOGLE OAUTH ====================
    GOOGLE_CLIENT_ID: str = Field(
        "",
        description="Google OAuth client ID (optional)"
    )
    GOOGLE_CLIENT_SECRET: str = Field(
        "",
        description="Google OAuth client secret (optional)"
    )

    # ==================== APPLICATION ====================
    PROJECT_NAME: str = Field(
        "AI Language Tutor",
        description="Project name for API docs"
    )
    DEBUG: bool = Field(
        False,
        description="Enable debug mode"
    )
    ENVIRONMENT: Literal["development", "staging", "production"] = Field(
        "development",
        description="Environment type"
    )

    # ==================== CORS & FRONTEND ====================
    FRONTEND_URLS: List[str] = Field(
        default=["http://localhost:3000"],
        description="Frontend URLs for CORS (independent from backend)"
    )

    # ==================== LOGGING ====================
    LOG_LEVEL: str = Field(
        "INFO",
        description="Logging level (DEBUG, INFO, WARNING, ERROR)"
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
        env_ignore_empty=False  # Fail if env vars missing
    )

    # ==================== VALIDATORS ====================

    @field_validator("SECRET_KEY")
    @classmethod
    def validate_secret_key(cls, v: str) -> str:
        """Ensure SECRET_KEY is strong"""
        if len(v) < 32:
            raise ValueError("SECRET_KEY must be at least 32 characters")
        return v

    @field_validator("DATABASE_URL")
    @classmethod
    def validate_database_url(cls, v: str) -> str:
        """Ensure DATABASE_URL uses PostgreSQL"""
        if not v.startswith(("postgresql://", "postgresql+asyncpg://")):
            raise ValueError(
                "DATABASE_URL must use PostgreSQL (postgresql:// or postgresql+asyncpg://)"
            )
        return v

    @field_validator("LOG_LEVEL")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Validate logging level"""
        valid_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        if v.upper() not in valid_levels:
            raise ValueError(f"LOG_LEVEL must be one of {valid_levels}")
        return v.upper()

    # ==================== PROPERTIES ====================

    @property
    def is_production(self) -> bool:
        """Check if running in production"""
        return self.ENVIRONMENT == "production"

    @property
    def is_development(self) -> bool:
        """Check if running in development"""
        return self.ENVIRONMENT == "development"

    @property
    def is_staging(self) -> bool:
        """Check if running in staging"""
        return self.ENVIRONMENT == "staging"


# Initialize and validate settings
try:
    settings = Settings()
    logger.success(f"✅ Settings loaded | Environment: {settings.ENVIRONMENT}")
except ValidationError as e:
    logger.error(f"❌ Settings validation failed:\n{e}")
    raise