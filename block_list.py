from aiogram import types
from users_storage_db import Database
import asyncio

db = Database('ShopDB.db')


async def usr_count_ban(message: types.Message):
    count = 1
    userban = db.get_blocked_users()
    if not userban:
        msg = await message.answer("Список пуст!")

    else:
        ban_list = []
        for user in userban:
            user_id = user["user_id"]
            full_name = user["full_name"]
            ban_list.append(f"{count}. *{full_name}*  `/unban {user_id}`")
            count += 1
        ban_list_str = "\n".join(ban_list)
        msg = await message.answer(f"Бан лист:\n{ban_list_str}", parse_mode='Markdown')
    await asyncio.sleep(5)
    await message.delete()
    await msg.delete()


def escape_markdown(text):
    return text.replace('_', '')


async def usr_list(message: types.Message):
    users = db.get_unblocked_users()
    if not users:
        await message.answer("Список пуст!")
        return
    page_size = 50
    for i in range(0, len(users), page_size):
        page = users[i:i + page_size]
        text_lines = [f"{num}. _{escape_markdown(u['full_name'])}_ `/ban {u['user_id']}`"
                      for num, u in enumerate(page, start=i + 1)]
        text = '\n'.join(text_lines)
        await message.answer(f"Список пользователей (стр. {i // page_size + 1}):\n{text}", parse_mode='Markdown')


async def unban_user(message: types.Message):
    args = message.get_args()
    if not args:
        pass
    else:
        user_id = args
        db.user_un_ban(user_id)
        msg = await message.answer("Пользователь разблокирован!")
        await asyncio.sleep(5)
        await message.delete()
        await msg.delete()


async def ban_user(message: types.Message):
    args = message.get_args()
    if not args:
        pass
    else:
        user_id = args
        db.user_ban(user_id)
        msg = await message.answer("Пользователь блокирован!")
        await asyncio.sleep(5)
        await message.delete()
        await msg.delete()
