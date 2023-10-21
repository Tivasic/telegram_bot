import logging
import os

from pydantic import BaseSettings

APP_DIR: str = "D:\PycharmProjects\\telegram_bot"
CONFIG_ENV: str = os.getenv('CONFIG_ENV', '')

if not CONFIG_ENV:
    raise RuntimeError(
        'What is your environment local, prod or qa. '
        'You need to specify an environment variable "export CONFIG_ENV=?"'
    )

CONFIG_DIR = os.path.join(APP_DIR, 'configs', CONFIG_ENV, '.env')
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class Settings(BaseSettings):
    DB_HOST: str
    DB_NAME: str
    DB_USERNAME: str
    DB_PASSWORD: str
    TOKEN: str

    class Config:
        env_file: str = CONFIG_DIR


config = Settings()
