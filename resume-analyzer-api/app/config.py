from pydantic_settings import BaseSettings

class settings(BaseSettings):
    OPENAI_API_KEY: str
    MODEL:str = "gpt-4o-mini"

    class Config:
        env_file = ".env"

settings = settings()