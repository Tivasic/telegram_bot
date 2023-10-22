from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup


class MyDialog(StatesGroup):
    waiting_answer_event = State()
    waiting_reminder_event = State()


def get_unsupported_language_message():
    return "Supported languages are Russian or English.\nПоддерживаемые языки русский или английский."


class ManagerUser:
    def __init__(self, user_info):
        self.registration: bool = False
        self.language_code: str = user_info.language_code
        self.last_name: str = user_info.last_name
        self.first_name: str = user_info.first_name
        self.mention: str = user_info.mention
        self.id: int = user_info.id

    async def dialog_with_record(self, message: types.Message):
        if self.language_code in ('ru', 'eng'):
            await MyDialog.waiting_answer_event.set()
            await message.answer(self.get_dialog_message())
        else:
            await message.answer(get_unsupported_language_message())

    async def reminder_record(self, message: types.Message):
        if self.language_code in ('ru', 'eng'):
            await MyDialog.waiting_reminder_event.set()
            await message.answer(self.get_reminder_message())
        else:
            await message.answer(get_unsupported_language_message())

    async def show_all_records(self, all_records, message: types.Message):
        if self.language_code in ('ru', 'eng'):
            await message.answer("All your records:")
            await self.print_all_records(all_records, message)

    @staticmethod
    async def print_all_records(all_records, message: types.Message):
        records = []
        for i, record in enumerate(all_records, start=1):
            date = record[2].strftime("%Y-%m-%d %H:%M:%S")
            message_to_user = f"{i}. {date} - {record[1]}"
            records.append(message_to_user)
        await message.answer('\n'.join(records))

    def get_dialog_message(self):
        if self.language_code == 'ru':
            return "Введите информацию о событии.\nЧтобы выйти из режима добавления используйте: /stop\n"
        elif self.language_code == 'eng':
            return "Enter information about the event.\nTo exit the add mode, use: /stop"
        else:
            return get_unsupported_language_message()

    def get_reminder_message(self):
        if self.language_code == 'ru':
            return "Введите информацию о напоминании и дату в формате напоминание-дата\nЧтобы выйти из режима добавления используйте: /stop\n"
        elif self.language_code == 'eng':
            return "Enter information about reminder and date format reminder-date.\nTo exit the add mode, use: /stop"
        else:
            return get_unsupported_language_message()
