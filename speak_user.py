from date_time_online import online_date_time
from aiogram import types
from users_storage_db import Database
import aiogram.utils.exceptions
import time
from StoreBOT import bot
import asyncio
import os

db = Database()


# TODO вынести в отдельную
# async def speak_user(message: types.Message):
#     if not message.get_args():
#         await message.answer("Введите текст для рассылки `/speak_store Приветствую тебя!`", parse_mode='markdown')
#         return
#     users = db.get_users()
#     message_count = 0
#     for row in users:
#         try:
#             await bot.send_message(row[0], text=message.text[message.text.find(" "):])
#             message_count += 1
#             if int(row[1]) != 0:
#                 db.set_block(row[0], 0)
#         except aiogram.utils.exceptions.BotBlocked:
#             db.set_block(row[0], 1)
#         except aiogram.utils.exceptions.ChatNotFound:
#             db.delete_user(row[0])
#         except aiogram.utils.exceptions.UserDeactivated:
#             db.delete_user(row[0])
#         except aiogram.utils.exceptions.CantTalkWithBots:
#             db.delete_user(row[0])
#         except aiogram.utils.exceptions.RetryAfter as e:
#             await message.answer(f"Ожидание {e.timeout} секунд")
#             time.sleep(e.timeout)
#     await message.answer(f"Рассылка окончена.\nОтправлено сообщений: {message_count}")


async def save_photo(photo: types.PhotoSize):
    """Функция для сохранения фотографии в папку"""
    if not os.path.exists('img'):
        os.makedirs('img')
    file_id = photo.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    downloaded_file = await bot.download_file(file_path)
    file_name = 'send_img.jpg'
    with open(f'img/{file_name}', 'wb') as new_file:
        new_file.write(downloaded_file.read())


async def send_message_text(message: types.Message):
    await message.answer('Старт рассылки')
    _time = online_date_time()
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
    _time2 = online_date_time()
    await message.answer(f"Рассылка окончена.\n"
                         f"Отправлено сообщений: {message_count}\n"
                         f"Начало: {_time}MSK\n"
                         f"Окончание: {_time2}MSK")


async def send_message_photo_caption(photo, message: types.Message):
    await message.answer('Старт рассылки')
    _time = online_date_time()
    users = db.get_users()
    message_count = 0
    for row in users:
        try:
            with open(f'img/send_img.jpg', 'rb') as file:
                photo = types.InputFile(file)
                await bot.send_photo(row[0], photo, caption=message.text[message.text.find(" "):])
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

    _time2 = online_date_time()
    await message.answer(f"Рассылка окончена.\n"
                         f"Отправлено сообщений: {message_count}\n"
                         f"Начало: {_time}MSK\n"
                         f"Окончание: {_time2}MSK")
    os.remove(f'img/send_img.jpg')


async def speak_user(message: types.Message):
    if not message.get_args():
        await message.answer("Введите текст для рассылки `/speak_store Приветствую тебя!`", parse_mode='markdown')
        return

    file_name = 'send_img.jpg'

    if os.path.exists(f'img/{file_name}'):
        with open(f'img/{file_name}', 'rb') as file:
            photo = types.InputFile(file)
        print(f"Файл '{file_name}' существует в папке 'img'")
        _ = asyncio.create_task(send_message_photo_caption(photo, message))

    else:
        print(f"Файл '{file_name}' не найден в папке 'img'")
        _ = asyncio.create_task(send_message_text(message))


async def speakclear(message: types.Message):
    try:
        os.remove(f'img/send_img.jpg')
        await message.answer("Медиа для рассылки удалено!")
    except Exception:
        await message.answer("Медиа отсутствует")
