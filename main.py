import asyncio
import platform

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

from bot_manager import BotManager
from db_manager import DbManager
from game_manager import DiceGame
from user_manager import UserManagerUser, Mydialog
from utils import logging

bot = Bot(token=BotManager().get_token())

db = DbManager()
dp = Dispatcher(bot, storage=MemoryStorage())
user = UserManagerUser()


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.message):
    await user.info_about_user(message)
    logging.info(f'Бот поздоровался с пользователем: {user.mention, user.id}')

    user.registration = await db.checking_registration(user)
    if user.registration is True:
        if user.language_code != 'ru':
            await message.answer("Hi!\n"
                                 "You have successfully logged in\n"
                                 "To view the list of commands, use: /help")

        await message.answer(f'Привет!\n')
        await message.answer(f'Вы успешно авторизовались!\n'
                             f'Теперь я ваш ежедневник\n'
                             f'Чтобы посмотреть список комманд используйте: /help')
    else:
        if await db.register_user(user) is True:
            user.registration = True
            await message.answer(f'Вы успешно зарегистрировались!\n'
                                 f'Чтобы посмотреть список комманд используйте: /help')
        else:
            await message.answer(f'Не удалось зарегистрироваться. Повторите попытку позднее!\n')


@dp.message_handler(commands=['help'])
async def help_commands(message: types.message):
    await user.info_about_user(message)
    if user.registration is True:
        await message.answer(f'(Бета)Чтобы добавить запись о событии используйте: /add_record\n'
                             f'(Бета)Чтобы посмотреть все записи за все время используйте: /show_all_records\n'
                             f'(В будущем)Чтобы создать напоминание о событии используйте: /add_reminder\n'
                             f'Чтобы поиграть с ботом в кости используйте: /dice_game')
    else:
        await message.answer(f'Вам необходимо перезапустить бота и авторизоваться: /start\n')


@dp.message_handler(commands=['add_record'])
async def add_record(message: types.message):
    await user.info_about_user(message)
    if user.registration is True:
        await user.dialog_with_record(message)
    else:
        await message.answer(f'Вам необходимо перезапустить бота и авторизоваться: /start\n')


@dp.message_handler(commands=['show_all_records'])
async def show_all_records(message: types.message):
    await user.info_about_user(message)
    if user.registration is True:
        all_records = await db.get_all_records(user)
        if all_records:
            await user.show_all_records(all_records, message)
        else:
            await message.answer(f'Вы не добавили еще ни одной записи. Используйте: /add_record\n')
    else:
        await message.answer(f'Вам необходимо перезапустить бота и авторизоваться: /start\n')


@dp.message_handler(commands=['add_reminder'])
async def add_reminder(message: types.message):
    await user.info_about_user(message)
    if user.registration is True:
        await message.answer('В разработке')
    else:
        await message.answer(f'Вам необходимо перезапустить бота и авторизоваться: /start\n')


@dp.message_handler(commands=['dice_game'])
async def dice_game(message: types.message):
    if user.registration is True:
        await asyncio.gather(DiceGame.start_game(bot, message))
        await message.answer(f'Хотите сыграть еще раз? Используйте: /dice_game\n'
                             f'Или вернитесь к списку команд: /help\n')
    else:
        await message.answer(f'Вам необходимо перезапустить бота и авторизоваться: /start\n')


@dp.message_handler(state=Mydialog.waiting_answer_event)
async def process_message(message: types.Message, state: FSMContext):
    await user.info_about_user(message)
    async with state.proxy() as data:
        data['text'] = message.text
        user_message = data['text']
        if user_message in ['/stop', 'stop']:
            await message.answer(f'Вы отменили добавление записи.\n')
            await state.finish()
            return
        elif user_message.find('/') != -1:
            await message.answer(f'Введите сообщение правильно.\n')
            return
        await db.add_record(user_message, user)
        await message.answer(f'Вы успешно добавили запись о событии. \n'
                             f'Чтобы посмотреть все ваши записи используйте: /show_all_records\n')
        await state.finish()


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
