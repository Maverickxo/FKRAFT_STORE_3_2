import random
import asyncio
import datetime
import sqlite3
from aiogram import types
from StoreBOT import bot

users = []

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
    {12: 'Двенадцать! Невероятная удача, поздравляю!\nКупон отправлен в личку! '}
]


async def count_user_dice_data(message):
    date = datetime.date.today()
    formatted_date = date.strftime("%Y-%m-%d")
    conn = sqlite3.connect('ShopDB.db')
    curs = conn.cursor()
    curs.execute(f"SELECT last_roll_date, full_name FROM dice_rolls WHERE last_roll_date = '{formatted_date}' ")
    data1 = curs.fetchall()
    await count_user_win(data1, message)


async def count_user_win(data1, message):
    conn = sqlite3.connect('ShopDB.db')
    curs = conn.cursor()
    curs.execute("SELECT full_name, count_win FROM dice_rolls WHERE count_win >= 1")
    data = curs.fetchall()
    await print_list_user_dice(data, data1, message)


async def user_count_dice_win_and_alldice(user_id):
    conn = sqlite3.connect('ShopDB.db')
    cursor = conn.cursor()
    cursor.execute('SELECT count_dice, count_win FROM dice_rolls WHERE user_id = ?', (user_id,))
    user_data = cursor.fetchone()
    all_count = user_data[0]
    win_count = user_data[1]
    return all_count, win_count


async def write_user_last_time(user_id, current_date, user_name, full_name):
    conn = sqlite3.connect('ShopDB.db')
    cursor = conn.cursor()
    cursor.execute('SELECT user_id FROM dice_rolls WHERE user_id = ?', (user_id,))
    existing_user = cursor.fetchone()
    if existing_user:
        cursor.execute(
            'UPDATE dice_rolls SET last_roll_date = ?, user_name = ?, full_name = ? WHERE user_id = ?',
            (current_date, user_name, full_name, user_id))
    else:
        cursor.execute(
            'INSERT INTO dice_rolls (user_id, last_roll_date, user_name, full_name) VALUES (?, ?, ?, ?)',
            (user_id, current_date, user_name, full_name))
    conn.commit()
    conn.close()


async def increment_user_count_dice(user_id):
    conn = sqlite3.connect('ShopDB.db')
    cursor = conn.cursor()
    cursor.execute('SELECT count_dice FROM dice_rolls WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()

    if result is not None:
        current_count = result[0]
        new_count = current_count + 1
        cursor.execute('UPDATE dice_rolls SET count_dice = ? WHERE user_id = ?', (new_count, user_id))
        print(new_count)
        conn.commit()
    else:
        print(f"[Пользователь с user_id {user_id} не найден.]")
    conn.close()


async def increment_user_count_win(user_id):
    conn = sqlite3.connect('ShopDB.db')
    cursor = conn.cursor()
    cursor.execute('SELECT count_win FROM dice_rolls WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    if result is not None:
        current_count = result[0]
        new_count = current_count + 1
        cursor.execute('UPDATE dice_rolls SET count_win = ? WHERE user_id = ?', (new_count, user_id))
        conn.commit()
    else:
        print(f"Пользователь с user_id {user_id} не найден.")
    conn.close()


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
    user_id = message.from_user.id
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
        await bot.send_message(user_id, response + '*\nКоманда для проверки купона: /ck_coupon\n*'
                               , parse_mode='markdown')

    else:
        await message.answer("Нет доступных купонов")


# /dice

async def send_dice(message: types.Message):
    await message.delete()
    current_date = datetime.datetime.now().date()
    user_id = message.from_user.id
    user_name = message.from_user.mention
    full_name = message.from_user.full_name
    if user_id == 405223969:
        with open("krit.png", 'rb') as photo_file:
            await message.answer_photo(photo_file, caption=f'Поздравим победителя {full_name}')

    else:
        try:
            if await can_throw_dice(user_id):
                bot_data1 = await message.answer_dice()
                dice_value1 = bot_data1.dice.value
                bot_data2 = await message.answer_dice()
                dice_value2 = bot_data2.dice.value
                game_over = dice_value1 + dice_value2
                print(f"Сумма: {game_over}")
                await increment_user_count_dice(user_id)

                if game_over == 12:
                    await write_user_last_time(user_id, current_date, user_name, full_name)
                    await asyncio.sleep(3.70)
                    game_info = status[game_over - 1][game_over]
                    all_count, win_count = await user_count_dice_win_and_alldice(user_id)

                    msg = await message.answer(
                        f"{full_name}\n\nПобеда {game_info}\n\nВсего бросков: {all_count}\nВыигрышных бросков: {win_count}")

                    await increment_user_count_win(user_id)
                    await get_user_coupons(message)
                    # await asyncio.sleep(30)
                    # await msg.delete()
                else:

                    await write_user_last_time(user_id, current_date, user_name, full_name)
                    game_info = status[game_over - 1][game_over]
                    await asyncio.sleep(3.70)

                    all_count, win_count = await user_count_dice_win_and_alldice(user_id)
                    await zarik_money(message, game_over, user_id, game_info, full_name, game_over, all_count,
                                      win_count)


                    await asyncio.sleep(30)
                    await bot_data1.delete()
                    await bot_data2.delete()

            else:
                msg = await message.answer("Вы уже бросили кубики сегодня. Попробуйте завтра!")
                await asyncio.sleep(10)
                await msg.delete()
        except:
            pass


# /dice_list
async def print_list_user_dice(data, data1, message: types.Message):
    await message.delete()
    users_data = ""
    cont = 0
    users_data += f"Список пользователей получивших купон :\n\n"
    for x in data:
        if x[1] >= 1:
            cont += 1
            users.append([x[0], x[1]])

    for user in users:
        users_data += f"{user[0]} - {user[1]} .шт\n"
    users_data += f'\nВсего пользователей: {cont} \n\n'
    if cont == 0:
        users_data += "нет пользователей\n"
    if data1:
        users_data += "Сегодня кидали кубы:\n"
        for x in data1:
            users.append([x[0], x[1]])
            users_data += f"{x[0]} {x[1]}\n"
    else:
        users_data += "Сегодня никто не кидал кубы\n"
    print(users_data)
    msg = await message.answer(users_data)
    users.clear()
    await asyncio.sleep(40)
    await msg.delete()


async def zarik_money(message: types.Message, money, user_id, game_info, full_name, game_over, all_count,
                      win_count):
    conn = sqlite3.connect('ShopDB.db')
    cursor = conn.cursor()
    result = cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    row = result.fetchone()
    print(row)
    if row is not None:
        print(row)
        cursor.execute("UPDATE users SET money = money + ? WHERE user_id = ?", (money, user_id))
        msg = await message.answer(
            f"{game_info}\n\n*{full_name}* Вы проиграли!\n\n"
            f"Вам начислены коины: {game_over}\n"
            f"\nНе забывайте делится с другими участниками ответом "
            f"на сообщение пользователя` /send `100 \n\n"
            f"Всего бросков: {all_count}\nВыигрышных бросков: {win_count}", parse_mode='markdown')
        await asyncio.sleep(30)
        await msg.delete()
    else:
        await message.answer('Вы не найдены в базе магазина, '
                             'коины не будут начислены, '
                             'примите правила магазина! '
                             '@KRAFT_STORE_BOT ')
        await asyncio.sleep(30)
        await message.delete()
    conn.commit()
    conn.close()
