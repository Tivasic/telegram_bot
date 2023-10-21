from functools import wraps

from aiogram.dispatcher import FSMContext

from models.user import User
from user_manager import ManagerUser


def initialize_user_if_not_exists(func):
    @wraps(func)
    async def wrapper(message, state: FSMContext, *args, **kwargs):

        if not await state.get_data():
            async with state.proxy() as data:
                user_info = User.parse_obj(message.from_user)
                user = ManagerUser(user_info)
                data['user'] = user
        else:
            async with state.proxy() as data:
                user = data.get('user')

        result = await func(message, state, user, *args, **kwargs)
        return result

    return wrapper


def update_user_data_on_completion(func):
    @wraps(func)
    async def wrapper(message, state: FSMContext, user, *args, **kwargs):
        initial_registration = user.registration

        result = await func(message, state, user, *args, **kwargs)
        if user.registration != initial_registration:
            async with state.proxy() as data:
                user_data = data.get('user')
                if user_data is None or user_data.registration != user.registration:
                    data['user'] = user

        return result

    return wrapper
