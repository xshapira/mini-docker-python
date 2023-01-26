import functools

from pydantic import BaseSettings


class Settings(BaseSettings):
    KAFKA_SERVER: str
    KAFKA_USERNAME: str
    KAFKA_PASSWORD: str

    class Config:
        case_sensitive = True
        env_file = ".env"


@functools.cache
def get_settings() -> Settings:
    """
    We're using `cache` decorator to re-use the same settings object,
    instead of reading it for each request. The Settings object will be
    created only once, the first time it's called. Then it will return
    the same object that was returned on the first call, again and again.
    """
    return Settings()


settings = get_settings()
