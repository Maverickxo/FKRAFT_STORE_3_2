from aiogram import types
from StoreBOT import bot
import aiogram.utils.exceptions
from connect_bd import connect_data_b
import asyncio

sale_swich = 0
sale_name = [{'12.12': 12}]


async def mesg_del_time(message: types.Message):
    await asyncio.sleep(20)
    await message.delete()


async def process_sale_message(message, text):
    msg = await message.answer(text)
    if msg is not None:
        _ = asyncio.create_task(mesg_del_time(msg))


def count_sale_day_coopon(count_cop):
    connection, cursor = connect_data_b()
    cursor.execute(f"SELECT COUNT(*) FROM coupons WHERE discount_percentage = %s", (count_cop,))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result[0]


async def count_pesent_coupon(message: types.Message):
    persen = message.get_args()
    if len(persen) == 0:
        await message.answer("Введите процент купона для подсчета `/count_cup x` ", parse_mode='markdown')
    elif not persen.isdigit():
        await message.answer("Введите число")
    else:
        await process_sale_message(message,
                                   f'Количество купонов на {persen}% : {count_sale_day_coopon(int(persen))} шт.')


async def sale_users_coopon(user_id, user_name, user_full_name, message: types.Message):
    connection, cursor = connect_data_b()

    cursor.execute("SELECT user_id FROM sale_users_day WHERE user_id = %s", (user_id,))

    result_user = cursor.fetchone()

    if result_user is None:

        cursor.execute("INSERT INTO sale_users_day (user_id, user_name, user_full_name) VALUES  (%s,%s,%s)",
                       (user_id, user_name, user_full_name))

        await select_coopon(message, user_id)

    else:

        await process_sale_message(message, f"{user_full_name} Вы уже брали купон по акции {list(sale_name[0])[0]}")

    cursor.close()
    connection.close()


async def select_coopon(message: types.Message, user_id):
    name_user = message.from_user.full_name
    connection, cursor = connect_data_b()
    cursor.execute(
        f"SELECT coupon_code FROM coupons WHERE discount_percentage = {sale_name[0][list(sale_name[0])[0]]} ORDER BY RANDOM()")
    result = cursor.fetchone()

    if result is None:
        await message.answer("Нет доступных купонов")
    else:
        try:
            await bot.send_message(user_id,
                                   f"Распродажа {list(sale_name[0])[0]}\n\n`{result[0]}` - {sale_name[0][list(sale_name[0])[0]]}%\n\n"
                                   f"Всего купонов осталось: *{count_sale_day_coopon(sale_name[0][list(sale_name[0])[0]])}*",
                                   parse_mode='markdown')
        except aiogram.utils.exceptions.BotBlocked:
            await process_sale_message(message,
                                       f"{name_user} Для получения необходимо разблокировать"
                                       f" бота или принять условия магазина!")

            cursor.execute("DELETE FROM sale_users_day WHERE user_id = %s", (user_id,))

        else:
            await message.answer(
                f"Распродажа {list(sale_name[0])[0]} активна\n\n{name_user}\nКупон отправлен в личку \n\n"
                f"Всего купонов осталось: {count_sale_day_coopon(sale_name[0][list(sale_name[0])[0]])}")
            return result[0]
    cursor.close()
    connection.close()


async def send_chat_link(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Перейти в чат магазина!", url='https://t.me/+9pic7uZH4y83OWVi'))
    await message.answer("Команда работает только в чате магазина!", reply_markup=keyboard)


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
        if message.chat.type != "private":
            if len(sale) == 0:
                await process_sale_message(message, 'Введите текущую акцию через пробел')
            elif sale not in sale_name[0]:
                await process_sale_message(message, f"{sale} - Такая акция не проводится")
            elif sale_swich == 1:
                await sale_users_coopon(user_id, user_name, user_full_name, message)
            else:
                await process_sale_message(message, "Распродажа не активна")
        else:
            await send_chat_link(message)
