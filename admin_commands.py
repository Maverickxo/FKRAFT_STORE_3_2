from StoreBOT import types
import aiogram.utils.exceptions

from keywords_dat import help_text
from connect_bd import connect_data_b
last_message = {}


async def handle_help_adm(message: types.Message):
    await message.answer(help_text)


async def product_list(message: types.Message):  # TODO готов
    connection, cursor = connect_data_b()
    global last_message
    chat_id = message.chat.id
    if chat_id in last_message and last_message[chat_id] is not None:
        try:
            await last_message[chat_id].delete()
        except aiogram.utils.exceptions.MessageToDeleteNotFound:
            pass
        except Exception as e:
            print(f"Ошибка при удалении предыдущего сообщения: {e}")
    cursor.execute("SELECT name, active FROM products ORDER BY id ASC")
    products_info = cursor.fetchall()
    if len(products_info) == 0:
        await message.answer("⚠️В магазине не добавлены товары⚠️\nдля добавления товара используйте |`/add_product`|",
                             parse_mode='markdown')
    else:

        keyboard = types.InlineKeyboardMarkup(row_width=1)
        for product in products_info:
            name = product[0]
            status = product[1]
            status_text = "включен" if status == 1 else "выключен"
            button_text = f"{name} - ({status_text})"
            button = types.InlineKeyboardButton(
                button_text, callback_data=f"change_status_{name}"
            )
            keyboard.add(button)
        msg = await message.answer("Выберите товар:", reply_markup=keyboard)
        last_message[chat_id] = msg
        await message.delete()


async def product_list_edit_price(message: types.Message):  # TODO готов
    connection, cursor = connect_data_b()
    global last_message
    chat_id = message.chat.id
    if chat_id in last_message and last_message[chat_id] is not None:
        try:
            await last_message[chat_id].delete()
        except aiogram.utils.exceptions.MessageToDeleteNotFound:
            pass
        except Exception as e:
            print(f"Ошибка при удалении предыдущего сообщения: {e}")

    cursor.execute("SELECT name, price FROM products")
    products_info = cursor.fetchall()

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    for product in products_info:
        name = product[0]
        price = product[1]
        button_text = f"{name} - {price} руб. ✍️"
        button = types.InlineKeyboardButton(
            button_text, callback_data=f"change_price_{name}"
        )
        keyboard.add(button)
    msg = await message.answer("Выберите товар:", reply_markup=keyboard)
    last_message[chat_id] = msg
    await message.delete()
