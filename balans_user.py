from aiogram import types
import sqlite3
from users_storage_db import Database
import asyncio

db = Database('ShopDB.db')


def escape_markdown(text):
    return text.replace('_', '')


async def set_money_to_zero(user_id):
    conn = sqlite3.connect("ShopDB.db")
    cursor = conn.cursor()

    try:
        # запрос на обновление баланса пользователя. Списываем в ноль
        cursor.execute("UPDATE users SET money=0 WHERE user_id=?", (user_id,))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Ошибка при выполнении запроса: {e}")
        return False
    finally:
        conn.close()


async def get_money_value_from_db(user_id):
    conn = sqlite3.connect("ShopDB.db")
    cursor = conn.cursor()

    try:

        cursor.execute("SELECT money FROM users WHERE user_id=?", (user_id,))
        result = cursor.fetchone()

        if result:
            money_value = result[0]
            return money_value
        else:
            # Если пользователя с указанным user_id нет в базе данных, вернем 0.
            return 0
    except sqlite3.Error as e:
        print(f"Ошибка при выполнении запроса: {e}")
    finally:
        conn.close()


async def usr_balans_list(message: types.Message):
    users = db.user_list_balans()
    if not users:
        await message.answer("Список пуст!")
        return
    page_size = 50
    for i in range(0, len(users), page_size):
        page = users[i:i + page_size]
        text_lines = [f"{num}. _{escape_markdown(u['full_name'])}_ `/add_user_balance {u['user_id']} {u['money']}`"
                      for num, u in enumerate(page, start=i + 1)]
        text = '\n'.join(text_lines)
        await message.answer(f"Список пользователей (стр. {i // page_size + 1}):\n{text}", parse_mode='Markdown')


async def add_user_balance_list(message: types.Message):
    conn = sqlite3.connect('ShopDB.db')
    cursor = conn.cursor()

    args = message.get_args().split()

    user_full_name = message.from_user.full_name
    if len(args) != 2:
        await message.answer("Неверный формат команды.\nИспользуйте: `/add_user_balance <id пользователя> <сумма>`",
                             parse_mode='Markdown')
        return

    user_id = args[0].strip()
    amount = args[1].strip()

    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()

    if result is None:
        await message.answer(f"Пользователь: {user_id} не найден")
        return

    try:
        amount = int(amount)
        if amount <= 0:
            raise ValueError

    except ValueError:
        await message.answer("Некорректная сумма, введите положительное число")
        return

    cursor.execute("UPDATE users SET money = money + ? WHERE user_id = ?", (amount, user_id))
    conn.commit()
    conn.close()
    money_value = await get_money_value_from_db(user_id)

    await message.answer(f"Баланс пользователя: *|{user_full_name}|*\n"
                         f"Пополнен на: {amount} успешно!\n"
                         f"Текущий баланс: {money_value}",
                         parse_mode='markdown')


async def add_deposit(message: types.Message):
    if message.reply_to_message is None:
        msg = await message.reply("Этой командой нужно отвечать на сообщение пользователя")
        await message.delete()
        await asyncio.sleep(5)
        await msg.delete()
        return

    if not message.get_args():
        msg = await message.reply("Укажите количество монет после команды")
        await message.delete()
        await asyncio.sleep(5)
        await msg.delete()
        return

    amount = int(message.get_args())
    try:
        amount = int(amount)
        if amount <= 0:
            raise ValueError

    except ValueError:
        msg = await message.reply("Неверное количество монет")
        await message.delete()
        await asyncio.sleep(5)
        await msg.delete()
        return

    user_id = message.reply_to_message.from_user.id

    conn = sqlite3.connect('ShopDB.db')
    cursor = conn.cursor()

    cursor.execute("UPDATE users SET money = money + ? WHERE user_id = ?", (amount, user_id))
    conn.commit()
    conn.close()

    user_name = message.reply_to_message.from_user.full_name

    msg = await message.reply(f"Вы начислили {amount} KRAFT coins пользователю {user_name}")
    await message.delete()
    await asyncio.sleep(5)
    await msg.delete()


async def check_user_money(message: types.Message):
    await message.delete()
    if message.reply_to_message and message.reply_to_message.from_user:

        repl_user_money = message.reply_to_message.from_user.id
        name_user_reply = message.reply_to_message.from_user.full_name
        conn = sqlite3.connect('ShopDB.db')
        cursor = conn.cursor()
        cursor.execute('SELECT money FROM users WHERE user_id=?', (repl_user_money,))
        money = cursor.fetchone()
        if money is None:
            msg = await message.answer("Пользователь не найден в магазине")
            await asyncio.sleep(10)
            await msg.delete()
        else:
            count_money = money[0]
            msg = await message.answer(f'Баланс: {name_user_reply}\nKRAFT coins: {count_money}')
            await asyncio.sleep(10)
            await msg.delete()
        conn.close()
    else:
        msg = await message.answer("Команда ответом на сообщение нужного юзера")
        await asyncio.sleep(10)
        await msg.delete()
