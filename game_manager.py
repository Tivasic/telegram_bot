from asyncio import sleep

from utils import logging


class DiceGame:
    @staticmethod
    async def start_game(bot, message):
        current_user = message.from_user
        logging.info(f'Пользователь: {current_user.mention, current_user.id}, решил поиграть в Dice')
        await message.answer('Начинаем игру!')
        await sleep(2)
        await message.answer('Бот кидает кубик!')
        await sleep(1)
        bot_dice = await bot.send_dice(current_user.id, allow_sending_without_reply=True)
        await sleep(5)
        await message.answer('Вы кидаете кубик!')
        await sleep(1)
        user_dice = await bot.send_dice(current_user.id, allow_sending_without_reply=True)
        await sleep(5)
        if bot_dice['dice']['value'] > user_dice['dice']['value']:
            await message.answer('Вы проиграли!')
        elif bot_dice['dice']['value'] < user_dice['dice']['value']:
            await message.answer('Вы победили!')
        else:
            await message.answer('Ничья')
