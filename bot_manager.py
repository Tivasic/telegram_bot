"""Содержит базовую реализацию менеджера бота при помощи паттерна Одиночка"""
import logging
from configparser import ConfigParser


class BotManagerMeta(type):
    _instances = None

    def __call__(cls, *args, **kwargs):
        if cls._instances is None:
            cls._instances = super().__call__(*args, **kwargs)
        return cls._instances


class BotManager(metaclass=BotManagerMeta):
    def __init__(self):
        self.bot_token = None

    def get_token(self):
        if self.bot_token is None:
            try:
                config = ConfigParser()
                config.read('bot_settings.conf')
                self.set_token(config)
            except Exception as ex:
                logging.error(ex)
        return self.bot_token

    def set_token(self, config):
        self.bot_token = config['DATA']['TOKEN']
