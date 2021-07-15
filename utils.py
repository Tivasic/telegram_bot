"""
Служебные утилиты.
"""
import configparser

from celery.utils.log import get_task_logger
import logging as log_lib
from logging import handlers

config = configparser.ConfigParser()
config.read('bot_settings.conf')

logging = get_task_logger(__name__)
try:
    level = config['logger_root']['level']
    logging.setLevel(level)
    file_handler = log_lib.handlers.TimedRotatingFileHandler('bot_working.log', encoding='utf-8')
    stream_handler = log_lib.StreamHandler()
    stream_handler.setLevel(level)
    file_handler.setLevel(log_lib.DEBUG)

    formatter = log_lib.Formatter(f'%(asctime)s - %(levelname)s - %(message)s - [%(filename)s:%(lineno)d]')

    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)
    logging.addHandler(stream_handler)
    logging.addHandler(file_handler)
except KeyError:
    pass
