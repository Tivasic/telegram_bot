import logging
from asyncio import sleep

logger = logging.getLogger(__name__)


class DiceGame:
    @staticmethod
    async def start_game(bot, message):
        current_user = message.from_user
        logger.info(f'Пользователь: {current_user.mention, current_user.id}, решил поиграть в Dice')

        # Сообщения и ожидания
        game_start_message = 'Начинаем игру!'
        bot_dice_message = 'Бот кидает кубик!'
        user_dice_message = 'Вы кидаете кубик!'
        lose_message = 'Вы проиграли!'
        win_message = 'Вы победили!'
        draw_message = 'Ничья'

        await message.answer(game_start_message)
        await sleep(2)

        await message.answer(bot_dice_message)
        await sleep(1)
        bot_dice = await DiceGame.roll_dice(bot, current_user.id)
        await sleep(5)

        await message.answer(user_dice_message)
        await sleep(1)
        user_dice = await DiceGame.roll_dice(bot, current_user.id)
        await sleep(5)

        if bot_dice > user_dice:
            await message.answer(lose_message)
        elif bot_dice < user_dice:
            await message.answer(win_message)
        else:
            await message.answer(draw_message)

    @staticmethod
    async def roll_dice(bot, user_id):
        dice = await bot.send_dice(user_id, allow_sending_without_reply=True)
        return dice['dice']['value']
