from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    API_PORT: int
    ROOT_PATH: str = "/fiap-soad"
    MONGO_URI: str | None = None
    MONGO_URL: str | None = None
    MONGO_PORT: int | None = None
    MONGO_USERNAME: str | None = None
    MONGO_PASSWORD: str | None = None
    MONGO_DATABASE: str | None = None

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings():
    return Settings()
