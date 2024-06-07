import functools
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent
DOTENV_FILE = Path(BASE_DIR, ".env")
DOTENV_PROD = Path(BASE_DIR, "prod.env")


class Settings(BaseSettings):
    DEBUG: bool = Field(default=...)
    RABBITMQ_HOST: str = Field(default=...)
    RABBITMQ_USERNAME: str = Field(default=...)
    RABBITMQ_PASSWORD: str = Field(default=...)
    RABBITMQ_PORT: int = Field(default=...)
    RABBITMQ_VHOST: str = Field(default=...)

    model_config = SettingsConfigDict(case_sensitive=True, env_file=DOTENV_FILE)


@functools.cache
def get_settings() -> Settings:
    """
    We're using `cache` decorator to re-use the same settings object,
    instead of reading it for each request. The Settings object will be
    created only once, the first time it's called. Then it will return
    the same object that was returned on the first call, again and again.
    """
    app_settings = Settings()
    if app_settings.DEBUG:
        return app_settings

    return Settings(_env_file=DOTENV_PROD, _env_file_encoding="utf-8")


settings = get_settings()
