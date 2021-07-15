import logging
from configparser import ConfigParser


class BotManager:

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



