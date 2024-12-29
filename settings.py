from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_title: str = "App Title"
    app_host: str = "0.0.0.0"
    app_port: int = 8000

    db_url: str = "sqlite+aiosqlite:///path/to/db.sqlite"

    redis_user: str = "user"
    redis_user_password: str = "password"
    redis_host: str = "localhost"
    redis_port: int = "6379"
    redis_todo_db_id: int | str = 0

    project_root: Path = Path(__file__).parent.resolve()

    model_config = SettingsConfigDict(env_file=".env", extra="allow")


settings = Settings()
