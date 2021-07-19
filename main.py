import asyncio
import platform

from aiogram import Bot, Dispatcher, executor, types

from bot_manager import BotManager
from db_manager import DbManager
from bot_games import DiceGame
from utils import logging

API_TOKEN = BotManager().get_token()
db = DbManager()

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.message):
    user_data = message.from_user
    logging.info(f'Бот поздоровался с пользователем: {user_data.mention, user_data.id}')
    if await db.checking_registration(user_data) is True:
        if user_data.language_code != 'ru':
            await message.answer("Hi!\n"
                                 "You have successfully logged in\n"
                                 "To view the list of commands, use: /help")

        await message.answer(f'Привет!\n')
        await message.answer(f'Вы успешно авторизовались!\n'
                             f'Теперь я твой ежедневник\n'
                             f'Чтобы посмотреть список комманд используй: /help')
    else:
        await db.register_user(user_data)
        await message.answer(f'Вы успешно зарегистрировались!\n'
                             f'Чтобы посмотреть список комманд используй: /help')


@dp.message_handler(commands=['help'])
async def help_commands(message: types.message):
    await message.answer(f'(В разработке)Чтобы добавить запись о событии используйте: /add_event\n'
                         f'(В разработке)Чтобы посмотреть все записи за все время используйте: /show_all_events\n'
                         f'(В разработке)Чтобы создать напоминание о событии используйте: /add_reminder\n'
                         f'Чтобы поиграть с ботом в кости используйте: /dice_game')


@dp.message_handler(commands=['add_event'])
async def add_event(message: types.message):
    await message.answer('В разработке')


@dp.message_handler(commands=['show_all_events'])
async def add_event(message: types.message):
    await message.answer('В разработке')


@dp.message_handler(commands=['add_reminder'])
async def add_event(message: types.message):
    await message.answer('В разработке')


@dp.message_handler(commands=['dice_game'])
async def dice_game(message: types.message):
    await asyncio.gather(DiceGame.start_game(bot, message))


def main():
    logging.info('App started')
    logging.debug("Machine: %s", platform.machine())
    logging.debug("version: %s", platform.version())
    logging.debug("platform: %s", platform.platform())
    logging.debug("uname: %s", platform.machine())
    logging.debug("system: %s", platform.system())
    executor.start_polling(dp, skip_updates=True)


if __name__ == '__main__':
    main()
