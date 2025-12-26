from typing import List, Optional

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True, extra="ignore")

    # API
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = False

    # CORS
    CORS_ORIGINS: List[str] = ["*"]

    # Pinecone
    PINECONE_API_KEY: str
    PINECONE_INDEX_NAME: str
    PINECONE_ENVIRONMENT: Optional[str] = None
    PINECONE_ENV: Optional[str] = None  # backward compat

    # OpenAI/LLM
    OPENAI_API_KEY: str
    LLM_MODEL: str = "gpt-3.5-turbo"
    EMBEDDING_MODEL: str = "text-embedding-3-small"
    EMBEDDING_DIM: int = 1024

    # Optional extras (ignored if not set)
    GOOGLE_API_KEY: Optional[str] = None
    FIREBASE_CREDS: Optional[str] = None

    # Rate limiting
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_WINDOW: int = 60  # seconds

    # Logging
    LOG_LEVEL: str = "INFO"

    @model_validator(mode="after")
    def populate_env_from_alias(self):
        # Allow PINECONE_ENV as alias for PINECONE_ENVIRONMENT
        if not self.PINECONE_ENVIRONMENT and self.PINECONE_ENV:
            self.PINECONE_ENVIRONMENT = self.PINECONE_ENV
        if not self.PINECONE_ENVIRONMENT:
            raise ValueError("PINECONE_ENVIRONMENT (or PINECONE_ENV) is required")
        return self


settings = Settings()


from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True, extra="ignore")

    # API
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = False

    # CORS
    CORS_ORIGINS: List[str] = ["*"]

    # Pinecone
    PINECONE_API_KEY: str
    PINECONE_INDEX_NAME: str
    PINECONE_ENVIRONMENT: Optional[str] = None
    PINECONE_ENV: Optional[str] = None  # backward compat

    # OpenAI/LLM
    OPENAI_API_KEY: str
    LLM_MODEL: str = "gpt-3.5-turbo"
    EMBEDDING_MODEL: str = "text-embedding-3-small"
    EMBEDDING_DIM: int = 1024

    # Optional extras (ignored if not set)
    GOOGLE_API_KEY: Optional[str] = None
    FIREBASE_CREDS: Optional[str] = None

    # Rate limiting
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_WINDOW: int = 60  # seconds

    # Logging
    LOG_LEVEL: str = "INFO"

    @model_validator(mode="after")
    def populate_env_from_alias(self):
        # Allow PINECONE_ENV as alias for PINECONE_ENVIRONMENT
        if not self.PINECONE_ENVIRONMENT and self.PINECONE_ENV:
            self.PINECONE_ENVIRONMENT = self.PINECONE_ENV
        if not self.PINECONE_ENVIRONMENT:
            raise ValueError("PINECONE_ENVIRONMENT (or PINECONE_ENV) is required")
        return self


settings = Settings()


from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True, extra="ignore")

    # API
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = False

    # CORS
    CORS_ORIGINS: List[str] = ["*"]

    # Pinecone
    PINECONE_API_KEY: str
    PINECONE_INDEX_NAME: str
    PINECONE_ENVIRONMENT: Optional[str] = None
    PINECONE_ENV: Optional[str] = None  # backward compat

    # OpenAI/LLM
    OPENAI_API_KEY: str
    LLM_MODEL: str = "gpt-3.5-turbo"
    EMBEDDING_MODEL: str = "text-embedding-3-small"
    EMBEDDING_DIM: int = 1024

    # Optional extras (ignored if not set)
    GOOGLE_API_KEY: Optional[str] = None
    FIREBASE_CREDS: Optional[str] = None

    # Rate limiting
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_WINDOW: int = 60  # seconds

    # Logging
    LOG_LEVEL: str = "INFO"

    @model_validator(mode="after")
    def populate_env_from_alias(self):
        # Allow PINECONE_ENV as alias for PINECONE_ENVIRONMENT
        if not self.PINECONE_ENVIRONMENT and self.PINECONE_ENV:
            self.PINECONE_ENVIRONMENT = self.PINECONE_ENV
        if not self.PINECONE_ENVIRONMENT:
            raise ValueError("PINECONE_ENVIRONMENT (or PINECONE_ENV) is required")
        return self


settings = Settings()

