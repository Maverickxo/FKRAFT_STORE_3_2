import sqlite3
from aiogram import types
from StoreBOT import bot


async def change_product_status(callback_query: types.CallbackQuery):
    product_name = callback_query.data.split("_")[2]
    conn = sqlite3.connect('ShopDB.db')
    current_status = conn.execute("SELECT active FROM products WHERE name = ?", (product_name,)).fetchone()[0]
    new_status = 1 if current_status == 0 else 0
    conn.execute("UPDATE products SET active = ? WHERE name = ?", (new_status, product_name))
    conn.commit()
    conn.close()
    status_text = "включен" if new_status == 1 else "выключен"
    new_button_text = f"{product_name} ({status_text})"
    keyboard = callback_query.message.reply_markup
    for row in keyboard.inline_keyboard:
        for button in row:
            if button.callback_data == callback_query.data:
                button.text = new_button_text
    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text="Выберите товар:",
        reply_markup=keyboard
    )

    await callback_query.answer(f"Статус товара успешно изменен - {product_name} ({status_text})")
