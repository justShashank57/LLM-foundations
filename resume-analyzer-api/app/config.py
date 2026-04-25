from pathlib import Path

from pydantic_settings import BaseSettings


ENV_FILE = Path(__file__).resolve().parents[2] / ".env"


class Settings(BaseSettings):
    OPENAI_API_KEY: str
    MODEL: str = "gpt-4o-mini"

    class Config:
        env_file = ENV_FILE


settings = Settings()
