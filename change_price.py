import sqlite3
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

class OrderForm(StatesGroup):
    EDIT_PRICE = State()


async def change_price(callback_query: types.CallbackQuery, state: FSMContext):
    product_name = callback_query.data.split('_')[2]
    await callback_query.message.answer(f"Введите новую цену для `|{product_name}|`:", parse_mode='markdown')

    await state.update_data(product_name=product_name)
    await OrderForm.EDIT_PRICE.set()


async def handle_new_price(message: types.Message, state: FSMContext):
    conn = sqlite3.connect('ShopDB.db')
    data = await state.get_data()
    product_name = data.get('product_name')
    new_price_text = message.text.strip()

    try:
        new_price = float(new_price_text)
        if new_price <= 0:
            raise ValueError()
    except ValueError:
        await message.answer("Некорректная цена.\nПожалуйста, введите положительное число.", parse_mode='markdown')
        return

    conn.execute("UPDATE products SET price = ? WHERE name = ?", (new_price, product_name))
    conn.commit()
    await message.answer(f"Цена для товара `|{product_name}|`\nобновлена: `|{new_price} руб.|`", parse_mode='markdown')
    await state.finish()
