from pydantic import BaseSettings


class Settings(BaseSettings):
    rabbitmq_host: str
    rabbitmq_username: str
    rabbitmq_password: str
    rabbitmq_port: int
    rabbitmq_vhost: str

    class Config:
        env_file = ".env"


settings = Settings()
