from aiogram import types
from StoreBOT import bot
import aiogram.utils.exceptions

from connect_bd import connect_data_b

sale_swich = 1
sale_name = ['11.11']


def count_sale_day_coopon():
    connection, cursor = connect_data_b()
    cursor.execute("SELECT COUNT(*) FROM coupons WHERE discount_percentage = 11")
    result = cursor.fetchone()
    return result[0]


async def sale_users_coopon(user_id, user_name, user_full_name, message: types.Message):
    connection, cursor = connect_data_b()

    result_user = cursor.execute("SELECT user_id FROM sale_users_day WHERE user_id = %s", (user_id,))

    result_user = cursor.fetchone()

    if result_user is None:

        cursor.execute("INSERT INTO sale_users_day (user_id, user_name, user_full_name) VALUES  (%s,%s,%s)",
                       (user_id, user_name, user_full_name))

        await select_coopon(message, user_id)

    else:

        await message.answer("Вы уже брали купон по акции 11.11 ")

    connection.close()


async def select_coopon(message: types.Message, user_id):
    name_user = message.from_user.full_name
    connection, cursor = connect_data_b()
    cursor.execute("SELECT coupon_code FROM coupons WHERE discount_percentage = 11 ORDER BY RANDOM()")
    result = cursor.fetchone()
    connection.close()
    if result is None:
        await message.answer("Нет доступных купонов")
    else:
        try:
            await bot.send_message(user_id,
                                   f"Распродажа 11.11\n\n`{result[0]}` - 11%\n\nВсего купонов осталось: *{count_sale_day_coopon()}*",
                                   parse_mode='markdown')
        except aiogram.utils.exceptions.BotBlocked:
            await message.answer(
                f"{name_user} Для получения необходимо разблокировать бота или принять условия магазина!")
            connection, cursor = connect_data_b()
            cursor.execute("DELETE FROM sale_users_day WHERE user_id = %s", (user_id,))
            connection.close()
        else:
            await message.answer(
                f"Распродажа 11.11 активна\n\nКупон отправлен в личку \n\nВсего купонов осталось: {count_sale_day_coopon()}")
            return result[0]


async def sale(message: types.Message):
    global sale_swich

    user_id = message.from_user.id
    user_name = message.from_user.mention
    user_full_name = message.from_user.full_name

    sale = message.get_args()
    await message.delete()
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
