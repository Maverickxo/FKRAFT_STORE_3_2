import random
import asyncio
import datetime
import sqlite3
from aiogram import types
from StoreBOT import bot

status = [
    {1: 'Один! Похоже, ты потратил весь фарт на сегодня'},
    {2: 'Два! Попробуй в другой раз'},
    {3: 'Тройка! Удача не на твоей стороне сегодня..'},
    {4: 'Четвёрка! Неплохо, но можно лучше'},
    {5: 'Пятёрка! Уже близко к успеху'},
    {6: 'Шестёрка! Ты на правильном пути'},
    {7: 'Семёрка! Везёт неплохо'},
    {8: 'Восьмёрка! Удача экономит на тебе'},
    {9: 'Девятка! Ты почти на вершине чемпион'},
    {10: 'Десятка! Время перестать играть в прятки с удачей'},
    {11: 'Одиннадцать! Вот это да, счастье нашло тебя, но нет..'},
    {12: 'Двенадцать! Невероятная удача, поздравляю!'}
]


async def wtite_user_last_time(user_id, current_date):
    conn = sqlite3.connect('ShopDB.db')
    cursor = conn.cursor()
    cursor.execute('INSERT OR REPLACE INTO dice_rolls (user_id, last_roll_date) VALUES (?, ?)',
                   (user_id, current_date))
    conn.commit()


async def can_throw_dice(user_id):
    conn = sqlite3.connect('ShopDB.db')
    cursor = conn.cursor()
    current_date = datetime.datetime.now().date()

    cursor.execute('SELECT last_roll_date FROM dice_rolls WHERE user_id = ?', (user_id,))
    last_roll_date = cursor.fetchone()
    conn.close()
    if last_roll_date is None:
        return True

    last_roll_date = datetime.datetime.strptime(last_roll_date[0], '%Y-%m-%d').date()

    if last_roll_date < current_date:
        return True
    else:
        return False


async def get_user_coupons(message: types.Message):
    conn = sqlite3.connect('ShopDB.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM coupons WHERE discount_percentage = 5 ORDER BY RANDOM() LIMIT 5")
    results_5_percent = cursor.fetchall()
    cursor.execute("SELECT * FROM coupons WHERE discount_percentage = 10 ORDER BY RANDOM() LIMIT 3")
    results_10_percent = cursor.fetchall()
    conn.close()
    all_results = results_5_percent + results_10_percent

    if all_results:
        random_coupons = random.sample(all_results, min(len(all_results), 1))

        response = ""
        for coupon in random_coupons:
            coupon_code = coupon[1]
            response += f"Код купона: `{coupon_code}`\n"

        await message.answer(response + '*\nКоманда для проверки купона: /ck_coupon\n*'
                             , parse_mode='markdown')

    else:
        await message.answer("Нет доступных купонов")


# /dice

async def send_dice(message: types.Message):
    await message.delete()
    current_date = datetime.datetime.now().date()
    user_id = message.from_user.id

    if await can_throw_dice(user_id):
        bot_data1 = await bot.send_dice(user_id)
        dice_value1 = bot_data1.dice.value
        bot_data2 = await bot.send_dice(user_id)
        dice_value2 = bot_data2.dice.value
        game_over = dice_value1 + dice_value2
        print(f"Сумма: {game_over}")

        if game_over == 12:
            await wtite_user_last_time(user_id, current_date)
            await asyncio.sleep(3.70)
            game_info = status[game_over - 1][game_over]
            msg = await message.answer(f"Победа {game_info}")

            await get_user_coupons(message)
            await asyncio.sleep(30)
            await msg.delete()
        else:
            await wtite_user_last_time(user_id, current_date)
            game_info = status[game_over - 1][game_over]
            await asyncio.sleep(3.70)
            msg = await message.answer(f"{game_info}\nВы проиграли!")
            await asyncio.sleep(30)
            await msg.delete()

    else:
        msg = await message.answer("Вы уже бросили кубики сегодня. Попробуйте завтра!")
        await asyncio.sleep(30)
        await msg.delete()
