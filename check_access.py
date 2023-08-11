from aiogram import types
from users_storage_db import Database

db = Database('ShopDB.db')

BAN_MSG = """
Извините, вы были заблокированы!\nОбратитесь к админам для получения информации.
"""


def check_ban_status(func):
    async def wrapper(message: types.Message, *args, **kwargs):
        user_id = message.from_user.id
        if db.check_ban_status(user_id):
            await message.answer(BAN_MSG)
        else:
            return await func(message, *args, **kwargs)

    return wrapper


def auth(func):
    allowed_ids = [5869013585, 5967935518, 1444325514]

    async def wrapper(message):
        if message['from']['id'] not in allowed_ids:
            return await message.reply("Доступ запрещен", reply=False)
        return await func(message)

    return wrapper


def aut_cgt():
    def decorator(func):
        async def wrapper(message: types.Message):
            if message.chat.type != types.ChatType.PRIVATE:
                pass
                return
            return await func(message)

        return wrapper

    return decorator


