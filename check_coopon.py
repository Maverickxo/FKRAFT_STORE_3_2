import asyncio
from aiogram import types
from connect_bd import connect_data_b


async def check_coupon(message: types.Message):
    if not message.get_args():
        msg = await message.answer("Вы не ввели код купона для проверки")

    else:
        coupon_code = message.get_args()
        connection, cursor = connect_data_b()
        cursor.execute("SELECT * FROM coupons WHERE coupon_code = %s", (coupon_code,))
        result = cursor.fetchone()
        if result:
            coupon_code_value = result[1]
            msg = await message.answer(f"Купон активен! `{coupon_code_value}`", parse_mode='markdown')
        else:
            msg = await message.answer("Купон не найден!")
        connection.close()
    await asyncio.sleep(20)
    await message.delete()
    await msg.delete()

# TODO готово!!
