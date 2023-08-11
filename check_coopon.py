import sqlite3
import asyncio
from aiogram import types

async def check_coupon(message: types.Message):
    if not message.get_args():
        msg = await message.answer("Вы не ввели код купона для проверки")

    else:
        coupon_code = message.get_args()
        conn = sqlite3.connect('ShopDB.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM coupons WHERE coupon_code = ?", (coupon_code,))
        result = cursor.fetchone()
        if result:
            msg = await message.answer("Купон активен!")
        else:
            msg = await message.answer("Купон не найден!")
        conn.close()
    await asyncio.sleep(5)
    await message.delete()
    await msg.delete()