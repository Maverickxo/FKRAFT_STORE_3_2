from aiogram import types, Bot
from users_storage_db import Database
import aiogram.utils.exceptions
import time
import config

bot = Bot(token=config.TOKEN)
db = Database('ShopDB.db')


async def speak_user(message: types.Message):
    if not message.get_args():
        await message.answer("Введите текст для рассылки `/speak Приветствую тебя!`", parse_mode='markdown')
        return
    users = db.get_users()
    message_count = 0
    for row in users:
        try:
            await bot.send_message(row[0], text=message.text[message.text.find(" "):])
            message_count += 1
            if int(row[1]) != 0:
                db.set_block(row[0], 0)
        except aiogram.utils.exceptions.BotBlocked:
            db.set_block(row[0], 1)
        except aiogram.utils.exceptions.ChatNotFound:
            db.delete_user(row[0])
        except aiogram.utils.exceptions.UserDeactivated:
            db.delete_user(row[0])
        except aiogram.utils.exceptions.CantTalkWithBots:
            db.delete_user(row[0])
        except aiogram.utils.exceptions.RetryAfter as e:
            await message.answer(f"Ожидание {e.timeout} секунд")
            time.sleep(e.timeout)
    await message.answer(f"Рассылка окончена.\nОтправлено сообщений: {message_count}")
