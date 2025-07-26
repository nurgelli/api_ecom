from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
import os

load_dotenv()


class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    PROJECT_NAME: str = 'FastAPI E-commerce'
    API_V1_STR: str = '/api/v1'
    
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: str = 30
    
    
    model_config = SettingsConfigDict(case_sensitive=True)

settings = Settings()
    
    
    