import platform

from aiogram import Bot, Dispatcher, executor, types

from bot_manager import BotManager
from utils import logging

bot_manager = BotManager()
API_TOKEN = bot_manager.get_token()

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.message):
    current_user = message.from_user
    logging.info(f'Бот поздоровался с пользователем: {current_user.mention, current_user.id}')
    if current_user.locale.language != 'ru':
        await message.reply("Hi!\nI'm Bot!\nPowered by aiogram.")
    await message.reply("Привет!\nЯ бот\nРаботаю на aiogramm.")


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
