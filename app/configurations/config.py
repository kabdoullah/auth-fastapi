import os
from pydantic_settings import BaseSettings, EmailStr

class ServerSettings(BaseSettings):
    PRODUCTION_SERVER: str
    PROD_PORT: int
    DEVELOPMENT_SERVER: str
    DEV_PORT: int

    class Config:
        env_file = os.getcwd() + '/configuration/server_settings.properties'

class DBSettings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    class Config:
        env_file = os.getcwd() + '/configuration/db_settings.properties'


class EmailSettings(BaseSettings):
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: EmailStr
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_FROM_NAME: str

    class Config:
        env_file = os.getcwd() + '/configuration/email_settings.properties'