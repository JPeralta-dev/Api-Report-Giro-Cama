from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )
    
    DB_DRIVER: str = ""
    DB_SERVER: str = ""
    DB_PORT: int = 1433
    DB_NAME: str = ""
    DB_USER: str = ""
    DB_PASSWORD: str = ""
    APP_ENV: str = "development"
    APP_PORT: int = 8000

    

settings = Settings()

