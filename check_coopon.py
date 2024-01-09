import asyncio
from aiogram import types
from connect_bd import connect_data_b
import re


async def check_coupon(message: types.Message):
    if not message.get_args():
        msg = await message.answer("Вы не ввели код купона для проверки")

    else:
        coupon_code = message.get_args()
        connection, cursor = connect_data_b()
        cursor.execute("SELECT * FROM coupons WHERE coupon_code = %s", (coupon_code,))
        result = cursor.fetchone()

        if result:
            coupon_code_value = result[1]
            msg = await message.answer(f"Купон активен! `{coupon_code_value}`", parse_mode='markdown')
        else:
            msg = await message.answer("Купон не найден!")
        cursor.close()
        connection.close()
    await asyncio.sleep(20)
    await message.delete()
    await msg.delete()


def check_coupon_in_db(coupon_code):
    try:
        connection, cursor = connect_data_b()

        if connection and cursor:
            cursor.execute("SELECT * FROM coupons WHERE coupon_code = %s", (coupon_code,))
            result = cursor.fetchone()

            if result:
                coupon_code_value = result[1]
                return f"Купон активен! `{coupon_code_value}` ✅"
            else:
                return f"Купон не найден! `{coupon_code}` ❌"
        else:
            return "Ошибка подключения к базе данных."

    except Exception as e:
        return f"Произошла ошибка при проверке купона: {e}"

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def find_and_check_coupons(text):
    combined_result = []

    coupon_pattern = re.compile(r'Код купона: ([A-Z0-9]+)')
    found_coupons = coupon_pattern.findall(text)

    if not found_coupons:
        return 'Коды купонов не обнаружены'

    for coupon in found_coupons:
        result = check_coupon_in_db(coupon)
        combined_result.append(result)

    combined_result = '\n'.join(combined_result)
    return combined_result
