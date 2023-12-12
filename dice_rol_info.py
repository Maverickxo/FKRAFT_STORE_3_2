import asyncio

from connect_bd import connect_data_b
import datetime
from aiogram import types


async def dice_rol_list_win(message: types.Message):
    """Список победителей"""
    connection, cursor = connect_data_b()
    users_data = ""
    count = 0
    cursor.execute(
        'SELECT count_dice, full_name, count_win FROM dice_rolls WHERE count_win > 0 ORDER BY count_win DESC')
    result = cursor.fetchall()
    for user in result:
        count += 1
        users_data += f"{count}.{user[1]} - {user[2]}|{user[0]} побед|бросков\n"
    print(f'Всего получило купоны: {count}\n\n{users_data}')
    msg = await message.answer(f'Всего получило купоны: {count}\n\n{users_data}')
    result.clear()
    cursor.close()
    connection.close()
    await asyncio.sleep(30)
    await msg.delete()


async def dice_rol_list(message: types.Message):
    """Список бросавших сегодня"""
    users_data = ""
    cont = 0
    connection, cursor = connect_data_b()
    date = datetime.date.today()
    formatted_date = date.strftime("%Y-%m-%d")
    cursor.execute(f"SELECT last_roll_date, full_name FROM dice_rolls WHERE last_roll_date = %s ",
                   (formatted_date,))

    result = cursor.fetchall()
    for user in result:
        cont += 1
        users_data += f'{cont}.{user[1]} \n'

    print(f'Сегодня бросали:\n\n{users_data}')
    msg = await message.answer(f'Сегодня бросали: {cont}\n\n{users_data}')
    result.clear()
    cursor.close()
    connection.close()
    await asyncio.sleep(30)
    await msg.delete()
