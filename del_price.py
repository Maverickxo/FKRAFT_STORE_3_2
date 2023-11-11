from aiogram import types
import sqlite3
import asyncio
from connect_bd import connect_data_b


async def del_price(message: types.Message):  # TODO Готов
    connection, cursor = connect_data_b()

    count = 1
    cursor.execute("SELECT name, active FROM products")
    result = cursor.fetchall()
    product_list = [{"name": row[0], "active": row[1]} for row in result]

    if not product_list:
        await message.answer("Список пуст!")
    else:
        price_list = []
        for product in product_list:
            product_name = product["name"]
            product_active = product["active"]
            price_list.append(f"{count}. `/del {product_name}` - {'активен' if product_active else 'неактивен'}")
            count += 1
        product_list_str = "\n".join(price_list)
        msg = await message.answer(f"Cписок товаров для удаления:\n{product_list_str}", parse_mode='Markdown')
        await asyncio.sleep(40)
        await msg.delete()
        await message.delete()


# Обработчик команды /del
async def delete_product(message: types.Message):  # TODO готов
    connection, cursor = connect_data_b()
    if message.get_args() == "":
        await message.answer("Введите название! `/del <название товара>`", parse_mode='Markdown')
        return

    product_name = message.text[5:].strip()  # Извлекаем название товара после /del
    # Проверяем, существует ли товар с таким названием в базе данных
    cursor.execute("SELECT name FROM products WHERE name = %s", (product_name,))
    result = cursor.fetchone()
    if result:
        # Удаляем товар из базы данных
        cursor.execute("DELETE FROM products WHERE name = %s", (product_name,))
        connection.close()
        msg = await message.answer(f"Товар `|{product_name}|` успешно удален.", parse_mode='Markdown')
    else:
        msg = await message.answer(f"Товар с названием `|{product_name}|` не найден.", parse_mode='Markdown')
    await asyncio.sleep(10)
    await msg.delete()
    await message.delete()
