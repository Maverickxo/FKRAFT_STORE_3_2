from aiogram import types
from keywords_dat import *


async def help_user(message: types.Message):
    btn_yes = types.InlineKeyboardButton(text="Вернутся к правилам", callback_data="rules_back")
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(btn_yes)
    await message.answer(HELP, parse_mode='markdown', reply_markup=keyboard)
