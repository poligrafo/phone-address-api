import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    app_name: str = "Phone Address API"
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    debug: bool = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.redis_host = os.getenv("REDIS_HOST", self.redis_host)
        self.redis_port = int(os.getenv("REDIS_PORT", self.redis_port))
        self.redis_db = int(os.getenv("REDIS_DB", self.redis_db))
        self.debug = bool(os.getenv("DEBUG", self.debug))

settings = Settings()
