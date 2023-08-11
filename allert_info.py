from keywords_dat import *
from aiogram import types
import time


async def alert_hd(message: types.Message):
    btn_alert_help = types.InlineKeyboardButton(text="«Не Нажимать!»", callback_data="rules_dumb")
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(btn_alert_help)

    with open("allert.jpg", 'rb') as photo_file:
        await message.answer_photo(photo_file, caption=ALERT_TEXT, parse_mode='markdown', reply_markup=keyboard)


async def dumb_msg(message: types.Message):
    with open("dumb.png", 'rb') as photo_file:
        del_msg = await message.answer_photo(photo_file)
        time.sleep(10)
        await del_msg.delete()
