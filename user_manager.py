"""Содержит базовую реализацию менеджера пользователя при помощи паттерна Одиночка"""

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup

from bot_manager import BotManager

bot = Bot(token=BotManager().get_token())
dp = Dispatcher(bot, storage=MemoryStorage())


class Mydialog(StatesGroup):
    waiting_answer_event = State()


class UserManagerUser:
    def __init__(self):
        self.first_name = None
        self.last_name = None
        self.mention = None
        self.language_code = None
        self.__id = None
        self.__registration = None

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, user_id):
        self.__id = user_id
        return

    @property
    def registration(self):
        return self.__registration

    @registration.setter
    def registration(self, flag):
        self.__registration = flag
        return

    @dp.message_handler()
    async def dialog_with_record(self, message: types.Message):
        if self.language_code == 'eng':
            await message.answer(f'Enter information about the event.\n'
                                 f'To exit the add mode, use: /stop')
            await Mydialog.waiting_answer_event.set()

        elif self.language_code == 'ru':
            await message.answer(f'Введите информацию о событии.\n'
                                 f'Чтобы выйти из режима добавления используйте: /stop\n')
            await Mydialog.waiting_answer_event.set()

        else:
            await message.answer(f'Supported languages are Russian or English.\n'
                                 f'Поддерживаемые языки русский или английский.\n')

    async def info_about_user(self, message: types.Message):
        self.id = message.from_user.id
        self.mention = message.from_user.mention
        self.first_name = message.from_user.first_name
        self.last_name = message.from_user.last_name

        if message.from_user.language_code == 'eng':
            self.language_code = 'eng'

        elif message.from_user.language_code == 'ru':
            self.language_code = 'ru'

    async def show_all_records(self, all_records, message: types.message):
        if self.language_code == 'eng':
            await message.answer("All your records:")
            await self.print_all_records(all_records, message)

        elif self.language_code == 'ru':
            await message.answer("Все ваши события:")
            await self.print_all_records(all_records, message)

    @staticmethod
    async def print_all_records(all_records, message: types.message):
        records = []
        for i, record in enumerate(all_records):
            date = record[2].strftime("%Y-%m-%d %H:%M:%S")
            data_record = i + 1, '.  ', date, ' - ', record[1]
            message_to_user = ''.join(map(str, data_record))
            records.append(message_to_user)
        await message.answer('\n'.join(records))
