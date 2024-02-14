# app/core/config.py
from typing import Optional

from dotenv import load_dotenv
from pydantic import BaseSettings, EmailStr

load_dotenv()


class Settings(BaseSettings):
    app_title: str = 'Благотворительный фонд поддержки котиков QRKot'
    description: str = 'Описание из .env'
    database_url: str = 'sqlite+aiosqlite:///./qrkot.db'
    secret: str = 'SECRET'
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None
    # Переменные для Google API
    type: Optional[str] = None
    project_id: Optional[str] = None
    private_key_id: Optional[str] = None
    private_key: Optional[str] = None
    client_email: Optional[str] = None
    client_id: Optional[str] = None
    auth_uri: Optional[str] = None
    token_uri: Optional[str] = None
    auth_provider_x509_cert_url: Optional[str] = None
    client_x509_cert_url: Optional[str] = None
    email: Optional[str] = None

    class Config:
        env_file = '.env'


settings = Settings()

# Константы
DEFAULT_AMOUNT = 0
MAX_LEN_NAME_PROJECT = 100
DEFAULT_INVESTED_STATUS = 0
# Параметры для гугл-таблиц
SCOPES = ['https://www.googleapis.com/auth/spreadsheets',
          'https://www.googleapis.com/auth/drive']
FORMAT = '%Y/%m/%d %H:%M:%S'  # Формат даты для имени файла
LOCALE = 'ru_RU'  # язык интерфейса
SHEET_ID = 0  # ID первого листа
SHEET_NAME = 'Лист1'
ROW_COUNT = 100
COLUMN_COUNT = 11
TABLE_RANGE = 'A1:E30'  # диапазон ячеек, в которые нужно внести изменения
SHEETS_API_VERSION = 'v4'
DRIVE_API_VERSION = 'v3'
