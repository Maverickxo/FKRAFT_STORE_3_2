from aiogram import types
from StoreBOT import bot
import aiogram
import time
import sqlite3


async def check_money_users(user_id, send_money):
    conn = sqlite3.connect('ShopDB.db')
    cursor = conn.cursor()
    cursor.execute('SELECT money FROM users WHERE user_id = ?', (user_id,))

    initial_balance_str = cursor.fetchone()[0]
    initial_balance = int(initial_balance_str)
    new_balance = initial_balance - int(send_money)

    conn.close()

    if new_balance == initial_balance:
        return True  # Баланс не изменился
    else:
        return False  # Баланс изменился


async def send_money_checker(message: types.Message):
    try:
        user_sender_money = message.from_user.full_name
        repl_user_id = message.reply_to_message.from_user.id
        if len(message.get_args().split()) != 1 or not message.get_args().isdigit():
            return
        else:
            money = message.get_args()
            # await check_money_users(repl_user_id, money)
            if await check_money_users(repl_user_id, money):
                await message.answer("не пополнен")
            else:
                msg_user_listed_money = f"Вам перечислено: {money} KRAFT conis\nот {user_sender_money}"
                await bot.send_message(repl_user_id, text=msg_user_listed_money)
    except aiogram.exceptions.CantInitiateConversation:
        pass
    except aiogram.exceptions.BotBlocked:
        pass
    except aiogram.exceptions.ChatNotFound:
        pass
    except aiogram.exceptions.UserDeactivated:
        pass
    except aiogram.exceptions.CantTalkWithBots:
        pass
    except aiogram.exceptions.RetryAfter as e:
        await message.answer(f"Ожидание {e.timeout} секунд")
        time.sleep(e.timeout)
