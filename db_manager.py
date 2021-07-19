import configparser

import psycopg2

from utils import logging


class DbManager:
    """
    Класс, осуществляющий запись данных в БД
    """

    def __init__(self):
        config = configparser.ConfigParser()
        config.read('bot_settings.conf')
        self._host = config['DATABASE']['DB_HOST']

        self._db_name = config['DATABASE']['DB_NAME']
        self._username = config['DATABASE']['DB_USERNAME']
        self._password = config['DATABASE']['DB_PASSWORD']

        try:
            self._connection = psycopg2.connect(
                host=self._host,
                database=self._db_name,
                user=self._username,
                password=self._password
            )
        except psycopg2.InterfaceError as ex:
            logging.error(ex)
            self._connection = None
        except psycopg2.OperationalError as ex:
            logging.error(ex)
            self._connection = None

    async def checking_registration(self, user_data):
        cursor = self._connection.cursor()
        uniquesql = '''SELECT * FROM users WHERE user_id=''' + str(user_data.id)
        cursor.execute(uniquesql)
        row = cursor.fetchall()
        if row:
            logging.debug(f'Пользователь: {user_data.mention, user_data.id} зарегистрирован')
            return True

    async def register_user(self, user_data):
        if not self._connection:
            logging.error("Не установлено соединение с БД")
            return
        if await self.checking_registration(user_data) is True:
            return True

        tsql = '''INSERT INTO users(user_id, first_name, last_name) VALUES (%s, %s, %s)'''

        user_id = user_data.id
        first_name = user_data.first_name
        last_name = user_data.last_name
        cursor = self._connection.cursor()

        try:
            cursor.execute(tsql, (user_id, first_name, last_name))
            logging.debug(f'Пользователь: {user_data.mention, user_data.id} зарегестрировался')
            self._connection.commit()

        except psycopg2.DatabaseError as ex:
            logging.error(ex, user_data)
            return
        return True
