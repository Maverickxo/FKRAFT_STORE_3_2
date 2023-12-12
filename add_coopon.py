from aiogram import types
import sqlite3
import random
from connect_bd import connect_data_b


# TODO модуль готов
def generate_coupon_code():
    return ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=20))


async def add_coupon(message: types.Message):  # TODO готов
    connection, cursor = connect_data_b()
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

    cursor.execute("SELECT * FROM coupons WHERE coupon_code = %s", (coupon_code,))
    existing_coupon = cursor.fetchone()
    if existing_coupon:
        await message.answer("Такой купон уже существует.")
        return
    try:
        cursor.execute("INSERT INTO coupons (coupon_code, discount_percentage) VALUES (%s, %s)",
                       (coupon_code, discount_percentage))

        await message.answer(
            f"Купон добавлен:\nКод купона: {coupon_code}\nПроцент скидки: {discount_percentage}%")
    finally:
        cursor.close()
        connection.close()


async def add_coupon_pack(message: types.Message):  # TODO готов
    connection, cursor = connect_data_b()
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
    try:
        for _ in range(int(coupon_count)):
            coupon_code = generate_coupon_code()
            cursor.execute('INSERT INTO coupons (coupon_code, discount_percentage) VALUES (%s, %s)',
                           (coupon_code, discount_percentage))
    finally:
        cursor.close()
        connection.close()

    await message.answer(
        f"Купоны добавлены: {coupon_count} шт.\nПроцент скидки: {discount_percentage}%")


async def add_coupon_off_time(message: types.Message):  # TODO готов
    connection, cursor = connect_data_b()
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
    try:
        cursor.execute("SELECT * FROM coupons WHERE coupon_code = %s", (coupon_code,))
        existing_coupon = cursor.fetchone()
        if existing_coupon:
            await message.answer("Такой купон уже существует.")

            return
        cursor.execute("INSERT INTO coupons (coupon_code, discount_percentage, off_time) VALUES (%s, %s, 1)",
                       (coupon_code, discount_percentage))

        await message.answer(
            f"Бессрочный купон добавлен:\nКод купона: *{coupon_code}*\nПроцент скидки: {discount_percentage}%",
            parse_mode='markdown')
    finally:
        cursor.close()
        connection.close()


async def delete_coupon_by_code(message: types.Message):  # TODO готов
    connection, cursor = connect_data_b()
    args = message.get_args().split()
    if len(args) != 1:
        await message.answer("Неверный формат команды.\nИспользуйте `/del_coupon_off_time <код купона>`",
                             parse_mode='markdown')
        return
    coupon_code = args[0].upper()
    try:

        cursor.execute("SELECT * FROM coupons WHERE coupon_code = %s", (coupon_code,))
        result = cursor.fetchone()
        if result:
            cursor.execute("DELETE FROM coupons WHERE coupon_code = %s", (coupon_code,))
            await message.answer(f"Купон `{coupon_code}` успешно удален.", parse_mode='markdown')
        else:

            await message.answer(f"Купон с кодом `{coupon_code}` не найден.", parse_mode='markdown')

    except sqlite3.Error as e:
        print("Ошибка удаления купона:", e)
        await message.answer("Произошла ошибка при удалении купона.")
    finally:
        cursor.close()
        connection.close()
