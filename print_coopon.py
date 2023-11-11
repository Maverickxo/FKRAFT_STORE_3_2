from aiogram import types
import random
import datetime
from keywords_dat import COUPON_TEXT
from connect_bd import connect_data_b


async def print_coupons(message: types.Message):  # TODO готов
    connection, cursor = connect_data_b()
    if not message.get_args():
        await message.answer("Введите скидку `/adm_get_coupons 5`", parse_mode='markdown')
    else:
        argument = message.get_args()

        cursor.execute("SELECT * FROM coupons WHERE discount_percentage = %s", (int(argument),))
        results = cursor.fetchall()
        if results:
            random_coupon = random.choice(results)
            coupon_code = random_coupon[1]
            await message.answer(
                f"Случайный купон на {argument}%:\nКод купона: {coupon_code}")
        else:
            await message.answer("Нет купонов с указанным процентом скидки")
        connection.close()


async def weekend_coupons(message: types.Message):  # TODO готов
    connection, cursor = connect_data_b()
    cursor.execute("SELECT * FROM coupons WHERE discount_percentage = 5 ORDER BY RANDOM() LIMIT 5")
    results_5_percent = cursor.fetchall()
    cursor.execute("SELECT * FROM coupons WHERE discount_percentage = 10 ORDER BY RANDOM() LIMIT 3")
    results_10_percent = cursor.fetchall()
    connection.close()
    all_results = results_5_percent + results_10_percent

    if all_results:
        random_coupons = random.sample(all_results, min(8, len(all_results)))
        response = f"Случайные купоны:\n(обновлены {datetime.datetime.now().strftime('%d.%m.%Y')})\n{COUPON_TEXT}"

        for coupon in random_coupons:
            # discount_percentage = coupon[2]
            coupon_code = coupon[1]
            response += f"Код купона: `{coupon_code}`\n"

        await message.answer(response + '*\nКоманда для проверки купона: /ck_coupon\n'
                                        'С уважением, Администрация!*', parse_mode='markdown')

    else:
        await message.answer("Нет доступных купонов")


async def print_coupons_off_time(message: types.Message):  # TODO готов
    connection, cursor = connect_data_b()
    cursor.execute("SELECT * FROM coupons WHERE off_time = 1")
    results = cursor.fetchall()
    if results:
        coupon_list = "\n".join(
            [f"Код Купона: {coupon[1]} - {coupon[2]}%  `/del_coupon_off_time {coupon[1]}`" for coupon in results])
        await message.answer(f"Список бессрочных купонов:\n\n{coupon_list}", parse_mode='markdown')
    else:
        await message.answer("Нет бессрочных купонов.")
    connection.close()
