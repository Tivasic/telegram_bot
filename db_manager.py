import configparser
import datetime

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

    async def checking_registration(self, user):
        if not self._connection:
            logging.error("Не установлено соединение с БД")
            return
        cursor = self._connection.cursor()
        uniquesql = '''SELECT * FROM users WHERE user_id=''' + str(user.id)
        cursor.execute(uniquesql)
        row = cursor.fetchall()
        if row:
            logging.debug(f'Пользователь: {user.mention, user.id} зарегистрирован')
            return True

    async def register_user(self, user):
        if not self._connection:
            logging.error("Не установлено соединение с БД")
            return
        if user.registration is True:
            return True
        tsql = '''INSERT INTO users(user_id, first_name, last_name) VALUES (%s, %s, %s)'''

        user_id = user.id
        first_name = user.first_name
        last_name = user.last_name
        cursor = self._connection.cursor()

        try:
            cursor.execute(tsql, (user_id, first_name, last_name))
            self._connection.commit()
            logging.debug(f'Пользователь: {user.mention, user.id} зарегистрировался')

        except psycopg2.DatabaseError as ex:
            logging.error(ex, user)
            return
        return True

    async def add_record(self, text_record, user):
        if not self._connection:
            logging.error("Не установлено соединение с БД")
            return
        if user.registration is True:
            tsql = '''INSERT INTO records(text_record, date_published, user_id_fk)
             VALUES (%s, %s, (SELECT id from users WHERE user_id=%s))'''

            user_id = user.id
            date_published = datetime.datetime.now()
            cursor = self._connection.cursor()

            try:
                cursor.execute(tsql, (text_record, date_published, user_id))
                self._connection.commit()
                logging.debug(f'Пользователь: {user.mention, user.id} успешно добавил запись о событии')

            except psycopg2.DatabaseError as ex:
                logging.error(ex, user)
                return
            return True

    async def get_all_records(self, user):
        if not self._connection:
            logging.error("Не установлено соединение с БД")
            return
        if user.registration is True:
            tsql = '''SELECT * FROM records WHERE user_id_fk = (SELECT id from users WHERE user_id=%s)'''

            user_id = user.id
            cursor = self._connection.cursor()

            try:
                cursor.execute(tsql, [user_id])
                self._connection.commit()
                all_records = cursor.fetchall()
                if all_records:
                    logging.debug(f'Пользователь: {user.mention, user.id} успешно получил все записи')
                    return all_records

            except psycopg2.DatabaseError as ex:
                logging.error(ex, user)
                return None
