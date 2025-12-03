from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables or .env file."""

    nginx_access_log_path: str = Field(
        default="/var/log/nginx/access.log",
        alias="NGINX_ACCESS_LOG_PATH",
        description="Path to nginx access log file.",
    )
    log_level: str = Field(
        default="INFO",
        alias="LOG_LEVEL",
        description="Logging level for the application.",
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
