import sqlite3
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


class OrderForm(StatesGroup):
    PRODUCT_NAME = State()
    NEW_PRICE = State()
    PRODUCT_ACTIVE = State()


def add_product(name, price, active):
    conn = sqlite3.connect('ShopDB.db')
    try:
        conn.execute("INSERT INTO products (name, price, active) VALUES (?, ?, ?)", (name, price, active))
        conn.commit()
        print("Товар успешно добавлен в базу данных.")
    except sqlite3.Error as e:
        print(f"Ошибка при добавлении товара в базу данных: {e}")
    finally:
        conn.close()


async def enter_product_name_handler(message: types.Message, state: FSMContext):
    # Сохраняем название товара в состоянии
    product_name = message.text.strip()
    await state.update_data(product_name=product_name)
    await message.answer("Введите цену товара:")
    await OrderForm.NEW_PRICE.set()


async def enter_product_price_handler(message: types.Message, state: FSMContext):
    # Сохраняем цену товара в состоянии
    if message.is_command():
        await message.reply("Это команда!")
        return
    try:
        product_price = float(message.text.strip())
        if product_price <= 0:
            raise ValueError()
    except ValueError:
        await message.answer("Некорректная цена. Пожалуйста, введите положительное число.")
        return
    await state.update_data(product_price=product_price)
    await message.answer("Товар активен? Введите 1, если активен, или 0, если неактивен:")
    await OrderForm.PRODUCT_ACTIVE.set()


async def enter_product_active_handler(message: types.Message, state: FSMContext):
    if message.is_command():
        await message.reply("Это команда!")
        return
    try:
        product_active = int(message.text.strip())
        if product_active not in (0, 1):
            raise ValueError()
    except ValueError:
        await message.answer("Некорректное значение активности. Введите 1, если товар активен, или 0, если неактивен.")
        return

    # Сохраняем активность товара в состоянии
    await state.update_data(product_active=product_active)

    # Получаем все данные о товаре из состояния
    data = await state.get_data()
    product_name = data.get('product_name')
    product_price = data.get('product_price')
    product_active = data.get('product_active')

    # Вызываем функцию для добавления товара в базу данных
    add_product(product_name, product_price, product_active)
    if product_active == 1:
        status = 'Активен'
    else:
        status = 'Не активен'
    await message.answer(
        f"Товар `|{product_name}:{product_price} руб.|` успешно добавлен в базу данных.\nСтатус: {status}",
        parse_mode='markdown')
    await state.finish()
