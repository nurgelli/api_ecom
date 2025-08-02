# app/core/config.py

from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
import os

load_dotenv() # .env dosyasını yüklüyor


class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    PROJECT_NAME: str = 'FastAPI E-commerce'
    API_V1_STR: str = '/api/v1'

    SECRET_KEY: str = os.getenv("SECRET_KEY") # Sınıf özelliği olarak tanımlandı
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 3000

    model_config = SettingsConfigDict(case_sensitive=True, extra='allow')

settings = Settings() # Ayarlar objesi burada oluşturuluyor ve yükleniyor

# print ifadesini buraya taşıyoruz
# Uygulamanın kullandığı kesin SECRET_KEY değerini görmek için:
print(f"DEBUG: Active SECRET_KEY is: {settings.SECRET_KEY}")