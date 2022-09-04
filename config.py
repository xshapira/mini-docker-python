import functools

from pydantic import BaseSettings


class Settings(BaseSettings):
    RABBITMQ_HOST: str
    RABBITMQ_USERNAME: str
    RABBITMQ_PASSWORD: str
    RABBITMQ_PORT: int
    RABBITMQ_VHOST: str

    class Config:
        case_sensitive = True
        env_file = ".env"


@functools.cache
def get_settings():
    """
    The Settings object will be created only once, the first time it's called.
    Then it will return the same object that was returned on the first call, again and again. We're using `cache` decorator to re-use the same settings object, instead of reading it for each request.
    """
    return Settings()


settings = get_settings()
