import datetime
import logging

import asyncpg as asyncpg

from config import config

logger = logging.getLogger(__name__)


class DbManager:
    def __init__(self):
        self._pool = None

    async def connect(self):
        try:
            self._pool = await asyncpg.create_pool(
                host=config.DB_HOST,
                database=config.DB_NAME,
                user=config.DB_USERNAME,
                password=config.DB_PASSWORD
            )
        except (asyncpg.InterfaceError, asyncpg.exceptions.ConnectionDoesNotExistError) as ex:
            logger.error(ex)

    async def close(self):
        if self._pool:
            await self._pool.close()

    async def execute_query(self, query, *params):
        if not self._pool:
            logger.error("Не установлено соединение с БД")
            return False

        async with self._pool.acquire() as connection:
            async with connection.transaction():
                result = await connection.fetch(query, *params)
                return result

    async def checking_registration(self, user):
        query = 'SELECT * FROM users WHERE id = $1'
        result = await self.execute_query(query, user.id)
        return bool(result)

    async def register_user(self, user):
        if user.registration:
            return True

        query = 'INSERT INTO users(id, first_name, last_name) VALUES($1, $2, $3)'
        params = (user.id, user.first_name, user.last_name)
        try:
            await self.execute_query(query, *params)
            logger.debug(f'Пользователь: {user.mention, user.id} зарегистрировался')
            return True
        except asyncpg.exceptions.PostgresError as ex:
            logger.error(ex)
            return False

    async def add_record(self, text_record, user):
        if not user.registration:
            return False

        query = 'INSERT INTO records(text_record, date_published, user_id_fk) VALUES($1, $2, (SELECT id FROM users WHERE id = $3))'
        params = (text_record, datetime.datetime.now(), user.id)
        try:
            await self.execute_query(query, *params)
            logger.debug(f'Пользователь: {user.mention, user.id} успешно добавил запись о событии')
            return True
        except asyncpg.exceptions.PostgresError as ex:
            logger.error(ex)
            return False

    async def get_all_records(self, user):
        if not user.registration:
            return None

        query = 'SELECT * FROM records WHERE user_id_fk = (SELECT id FROM users WHERE id = $1)'
        params = (user.id,)
        all_records = await self.execute_query(query, *params)
        logger.debug(f'Пользователь: {user.mention, user.id} успешно получил все записи')
        return all_records
