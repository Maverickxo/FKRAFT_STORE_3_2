from aiogram import types
import sqlite3
import random


async def add_coupon(message: types.Message):
    args = message.get_args().split()
    if len(args) != 2:
        await message.answer("Неверный формат команды.\nИспользуйте `/add_coupon <код купона> <процент скидки>`",
                             parse_mode='markdown')
        return
    coupon_code = args[0].strip().upper()
    discount_percentage = args[1].strip()
    try:
        discount_percentage = int(discount_percentage)
        if discount_percentage <= 0 or discount_percentage > 100:
            raise ValueError
    except ValueError:
        await message.answer("Некорректный процент скидки. Введите число от 1 до 100.")
        return
    conn = sqlite3.connect('ShopDB.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM coupons WHERE coupon_code = ?", (coupon_code,))
    existing_coupon = cursor.fetchone()
    if existing_coupon:
        await message.answer("Такой купон уже существует.")
        conn.close()
        return
    cursor.execute("INSERT INTO coupons (coupon_code, discount_percentage) VALUES (?, ?)",
                   (coupon_code, discount_percentage))
    conn.commit()
    conn.close()

    await message.answer(
        f"Купон добавлен:\nКод купона: {coupon_code}\nПроцент скидки: {discount_percentage}%")


def generate_coupon_code():
    return ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=16))


async def add_coupon_pack(message: types.Message):
    args = message.get_args().split()
    if len(args) != 2:
        await message.answer(
            "Неверный формат команды.\nИспользуйте `/add_coupon_pack <количество купонов> <процент скидки>`",
            parse_mode='markdown')
        return
    coupon_count = args[0].strip().upper()
    discount_percentage = args[1].strip()
    try:
        discount_percentage = int(discount_percentage)
        if discount_percentage <= 0 or discount_percentage > 100:
            raise ValueError
    except ValueError:
        await message.answer("Некорректный процент скидки. Введите число от 1 до 100.")
        return
    conn = sqlite3.connect('ShopDB.db')
    cursor = conn.cursor()
    for _ in range(int(coupon_count)):
        coupon_code = generate_coupon_code()
        cursor.execute('INSERT INTO coupons (coupon_code, discount_percentage) VALUES (?, ?)',
                       (coupon_code, discount_percentage))
    conn.commit()
    conn.close()

    await message.answer(
        f"Купоны добавлены: {coupon_count} шт.\nПроцент скидки: {discount_percentage}%")


async def add_coupon_off_time(message: types.Message):
    args = message.get_args().split()
    if len(args) != 2:
        await message.answer(
            "Неверный формат команды.\nИспользуйте `/add_coupon_off_time <код купона> <процент скидки>`",
            parse_mode='markdown')
        return
    coupon_code = args[0].strip().upper()
    discount_percentage = args[1].strip()
    try:
        discount_percentage = int(discount_percentage)
        if discount_percentage <= 0 or discount_percentage > 100:
            raise ValueError
    except ValueError:
        await message.answer("Некорректный процент скидки. Введите число от 1 до 100.")
        return
    conn = sqlite3.connect('ShopDB.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM coupons WHERE coupon_code = ?", (coupon_code,))
    existing_coupon = cursor.fetchone()
    if existing_coupon:
        await message.answer("Такой купон уже существует.")
        conn.close()
        return
    cursor.execute("INSERT INTO coupons (coupon_code, discount_percentage, off_time) VALUES (?, ?, 1)",
                   (coupon_code, discount_percentage))
    conn.commit()
    conn.close()

    await message.answer(
        f"Бессрочный купон добавлен:\nКод купона: *{coupon_code}*\nПроцент скидки: {discount_percentage}%",
        parse_mode='markdown')


async def delete_coupon_by_code(message: types.Message):
    args = message.get_args().split()
    if len(args) != 1:
        await message.answer("Неверный формат команды.\nИспользуйте `/del_coupon_off_time <код купона>`",
                             parse_mode='markdown')
        return

    coupon_code = args[0]
    conn = sqlite3.connect('ShopDB.db')
    cursor = conn.cursor()

    try:

        cursor.execute("SELECT * FROM coupons WHERE coupon_code = ?", (coupon_code,))
        result = cursor.fetchone()
        if result:
            cursor.execute("DELETE FROM coupons WHERE coupon_code = ?", (coupon_code,))
            conn.commit()
            conn.close()
            await message.answer(f"Купон `{coupon_code}` успешно удален.", parse_mode='markdown')
        else:
            conn.close()
            await message.answer(f"Купон с кодом `{coupon_code}` не найден.", parse_mode='markdown')

    except sqlite3.Error as e:
        print("Ошибка удаления купона:", e)
        conn.close()
        await message.answer("Произошла ошибка при удалении купона.")
