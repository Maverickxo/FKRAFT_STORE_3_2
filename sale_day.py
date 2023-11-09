import sqlite3
from aiogram import types
from StoreBOT import bot

sale_swich = 1
sale_name = ['11.11', '123', '333']


def bd_connect():
    conn = sqlite3.connect('ShopDB.db')
    cursor = conn.cursor()
    return cursor, conn


def count_sale_day_coopon():
    cursor, conn = bd_connect()
    cursor.execute("SELECT COUNT(*) FROM coupons WHERE discount_percentage = 11")
    result = cursor.fetchone()
    return result[0]


async def sale_users_coopon(user_id, user_name, user_full_name, message: types.Message):
    cursor, conn = bd_connect()
    result_user = cursor.execute(f"SELECT user_id FROM sale_users_day WHERE user_id = {user_id}").fetchone()
    if result_user is None:

        cursor.execute("INSERT INTO sale_users_day (user_id, user_name, user_full_name) VALUES  (?,?,?)",
                       (user_id, user_name, user_full_name))

        await select_coopon(message, user_id)

    else:

        await message.answer("Вы уже брали купон по акции 11.11 ")

    conn.commit()
    conn.close()


async def select_coopon(message: types.Message, user_id):
    cursor, conn = bd_connect()
    cursor.execute("SELECT coupon_code FROM coupons WHERE discount_percentage = 11 ORDER BY RANDOM()")
    result = cursor.fetchone()
    if result is None:
        await message.answer("Нет доступных купонов")
    else:

        await message.answer(
            f"Распродажа 11.11 активна\n\nКупон отправлен в личку \n\nВсего купонов осталось: {count_sale_day_coopon()}")
        await bot.send_message(user_id,
                               f"Распродажа 11.11\n\n{result[0]} - 11%\n\nВсего купонов осталось: {count_sale_day_coopon()}",
                               parse_mode='markdown')

        return result[0]
    conn.close()


async def sale(message: types.Message):
    global sale_swich

    user_id = message.from_user.id
    user_name = message.from_user.mention
    user_full_name = message.from_user.full_name

    sale = message.get_args()

    if sale.lower() == 'on':
        sale_swich = 1
        await message.answer("⚠️Распродажа активна⚠️")

    elif sale.lower() == 'off':
        sale_swich = 0
        await message.answer("⚠️Распродажа не активна⚠️")

    else:

        if len(sale) == 0:
            await message.answer('Введите текущую акцию через пробел')

        elif sale not in sale_name:
            await message.answer(f"{sale} - Такая акция не проводится")

        elif sale_swich == 1:
            await sale_users_coopon(user_id, user_name, user_full_name, message)

        else:
            await message.answer("Распродажа не активна")
