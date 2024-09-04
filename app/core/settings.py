from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Phone Address API"
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    debug: bool = True

    postgres_db: str = "postgres"
    postgres_user: str = "postgres"
    postgres_password: str = "password"
    postgres_port: int = 5433
    postgres_host: str = "db"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
