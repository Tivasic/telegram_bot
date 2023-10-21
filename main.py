import asyncio
import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

from config import config
from db_manager import DbManager
from decorators import initialize_user_if_not_exists, update_user_data_on_completion
from game_manager import DiceGame
from user_manager import ManagerUser, MyDialog

logger = logging.getLogger(__name__)
bot = Bot(token=config.TOKEN)

db = DbManager()
dp = Dispatcher(bot, storage=MemoryStorage())



@dp.message_handler(commands=['start'])
@initialize_user_if_not_exists
@update_user_data_on_completion
async def send_welcome(message: types.Message, state: FSMContext, user: ManagerUser):
    try:
        logger.info(f'Бот поздоровался с пользователем: {user.mention, user.id}')
        user.registration = await db.checking_registration(user)
        if not user.registration:
            user.registration = await db.register_user(user)
            await message.answer(f'Вы успешно зарегистрировались!\n'
                                 f'Чтобы посмотреть список команд используйте: /help')
        else:
            if user.language_code != 'ru':
                await message.answer("Hi!\n"
                                     "You have successfully logged in\n"
                                     "To view the list of commands, use: /help")
            else:
                await message.answer(f'Привет!\n')
                await message.answer(f'Вы успешно авторизовались!\n'
                                     f'Теперь я ваш ежедневник\n'
                                     f'Чтобы посмотреть список команд используйте: /help')

    except Exception as ex:
        logger.exception("Ошибка в команде /start: %s", ex)
        await message.answer("Произошла ошибка при выполнении команды /start. Пожалуйста, повторите попытку позднее.")


@dp.message_handler(commands=['help'])
@initialize_user_if_not_exists
@update_user_data_on_completion
async def help_commands(message: types.Message, state: FSMContext, user: ManagerUser):
    try:
        if user.registration:
            await message.answer(f'(Бета)Чтобы добавить запись о событии используйте: /add_record\n'
                                 f'(Бета)Чтобы посмотреть все записи за все время используйте: /show_all_records\n'
                                 f'(В будущем)Чтобы создать напоминание о событии используйте: /add_reminder\n'
                                 f'Чтобы поиграть с ботом в кости используйте: /dice_game')
        else:
            await message.answer(f'Вам необходимо перезапустить бота и авторизоваться: /start\n')
    except Exception as ex:
        logger.exception("Ошибка в команде /help: %s", ex)
        await message.answer("Произошла ошибка при выполнении команды /help. Пожалуйста, повторите попытку позднее.")


@dp.message_handler(commands=['add_record'])
@initialize_user_if_not_exists
@update_user_data_on_completion
async def add_record(message: types.Message, state: FSMContext, user: ManagerUser):
    try:
        if user.registration:
            await user.dialog_with_record(message)
        else:
            await message.answer(f'Вам необходимо перезапустить бота и авторизоваться: /start\n')

    except Exception as ex:
        logger.exception("Ошибка в команде /add_record: %s", ex)
        await message.answer(
            "Произошла ошибка при выполнении команды /add_record. Пожалуйста, повторите попытку позднее.")


@dp.message_handler(commands=['show_all_records'])
@initialize_user_if_not_exists
@update_user_data_on_completion
async def show_all_records(message: types.Message, state: FSMContext, user: ManagerUser):
    try:
        if user.registration:
            all_records = await db.get_all_records(user)
            if all_records:
                await user.show_all_records(all_records, message)
            else:
                await message.answer(f'Вы не добавили еще ни одной записи. Используйте: /add_record\n')
        else:
            await message.answer(f'Вам необходимо перезапустить бота и авторизоваться: /start\n')

    except Exception as ex:
        logger.exception("Ошибка в команде /show_all_records: %s", ex)
        await message.answer(
            "Произошла ошибка при выполнении команды /show_all_records. Пожалуйста, повторите попытку позднее.")


@dp.message_handler(commands=['add_reminder'])
@initialize_user_if_not_exists
@update_user_data_on_completion
async def add_reminder(message: types.Message, state: FSMContext, user: ManagerUser):
    try:
        if user.registration:
            await message.answer('В разработке')
        else:
            await message.answer(f'Вам необходимо перезапустить бота и авторизоваться: /start\n')

    except Exception as ex:
        logger.exception("Ошибка в команде /add_reminder: %s", ex)
        await message.answer(
            "Произошла ошибка при выполнении команды /add_reminder. Пожалуйста, повторите попытку позднее.")


@dp.message_handler(commands=['dice_game'])
@initialize_user_if_not_exists
@update_user_data_on_completion
async def dice_game(message: types.Message, state: FSMContext, user: ManagerUser):
    try:
        if user.registration:
            await asyncio.gather(DiceGame.start_game(bot, message))
            await message.answer(f'Хотите сыграть еще раз? Используйте: /dice_game\n'
                                 f'Или вернитесь к списку команд: /help\n')
        else:
            await message.answer(f'Вам необходимо перезапустить бота и авторизоваться: /start\n')

    except Exception as ex:
        logger.exception("Ошибка в команде /dice_game: %s", ex)
        await message.answer(
            "Произошла ошибка при выполнении команды /dice_game. Пожалуйста, повторите попытку позднее.")


@dp.message_handler(state=MyDialog.waiting_answer_event)
@initialize_user_if_not_exists
@update_user_data_on_completion
async def process_message(message: types.Message, state: FSMContext, user: ManagerUser):
    try:
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
    except Exception as ex:
        logger.exception("Ошибка в команде /add_record (ожидание ответа): %s", ex)
        await message.answer(
            "Произошла ошибка при выполнении команды /add_record (ожидание ответа). "
            "Пожалуйста, повторите попытку позднее."
        )


def main():
    logger.info('App started')
    loop = asyncio.get_event_loop()
    loop.run_until_complete(db.connect())
    executor.start_polling(dp, skip_updates=True)


if __name__ == '__main__':
    main()
