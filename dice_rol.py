import random
import asyncio
import datetime
from aiogram import types
from StoreBOT import bot
from connect_bd import connect_data_b
from dice_rol_info import dice_rol_list, dice_rol_list_win

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


async def user_count_dice_win_and_alldice(user_id):  # TODO Готов
    connection, cursor = connect_data_b()
    cursor.execute('SELECT count_dice, count_win FROM dice_rolls WHERE user_id = %s', (user_id,))
    user_data = cursor.fetchone()
    all_count = user_data[0]
    win_count = user_data[1]
    cursor.close()
    connection.close()
    return all_count, win_count


async def write_user_last_time(user_id, current_date, user_name, full_name):  # TODO Готов
    connection, cursor = connect_data_b()
    cursor.execute('SELECT user_id FROM dice_rolls WHERE user_id = %s', (user_id,))
    existing_user = cursor.fetchone()
    if existing_user:
        cursor.execute(
            'UPDATE dice_rolls SET last_roll_date = %s, user_name = %s, full_name = %s WHERE user_id = %s',
            (current_date, user_name, full_name, user_id))
    else:
        cursor.execute(
            'INSERT INTO dice_rolls (user_id, last_roll_date, user_name, full_name) VALUES (%s, %s, %s, %s)',
            (user_id, current_date, user_name, full_name))
    cursor.close()
    connection.close()


async def increment_user_count_dice(user_id):  # TODO Готоы
    connection, cursor = connect_data_b()
    cursor.execute('SELECT count_dice FROM dice_rolls WHERE user_id = %s', (user_id,))
    result = cursor.fetchone()

    if result is not None:
        current_count = result[0]
        new_count = current_count + 1
        cursor.execute('UPDATE dice_rolls SET count_dice = %s WHERE user_id = %s', (new_count, user_id,))
        print('Всего бросков', new_count)

    else:
        print(f"[Пользователь с user_id {user_id} не найден.]")
    cursor.close()
    connection.close()


async def increment_user_count_win(user_id):  # TODO Готоы
    connection, cursor = connect_data_b()
    cursor.execute('SELECT count_win FROM dice_rolls WHERE user_id = %s', (user_id,))
    result = cursor.fetchone()
    if result is not None:
        current_count = result[0]
        new_count = current_count + 1
        cursor.execute('UPDATE dice_rolls SET count_win = %s WHERE user_id = %s', (new_count, user_id,))

    else:
        print(f"Пользователь с user_id {user_id} не найден.")
    cursor.close()
    connection.close()


async def can_throw_dice(user_id):  # TODO Готоы
    connection, cursor = connect_data_b()
    current_date = datetime.datetime.now().date()

    cursor.execute('SELECT last_roll_date FROM dice_rolls WHERE user_id = %s', (user_id,))
    last_roll_date = cursor.fetchone()
    cursor.close()
    connection.close()

    if last_roll_date is None:
        return True

    last_roll_date = datetime.datetime.strptime(last_roll_date[0], '%Y-%m-%d').date()

    if last_roll_date < current_date:
        return True
    else:
        return False


async def get_user_coupons(message: types.Message):  # TODO Готоы
    connection, cursor = connect_data_b()
    user_id = message.from_user.id

    cursor.execute("SELECT * FROM coupons WHERE discount_percentage = 5 ORDER BY RANDOM() LIMIT 5")
    results_5_percent = cursor.fetchall()

    cursor.execute("SELECT * FROM coupons WHERE discount_percentage = 10 ORDER BY RANDOM() LIMIT 3")
    results_10_percent = cursor.fetchall()

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
    cursor.close()
    connection.close()


# Функция для отправки сообщения и его последующего удаления через 30 секунд
async def send_and_delete_message(message, text, delay=30):
    msg = await message.answer(text, parse_mode='markdown')
    await asyncio.sleep(delay)
    await msg.delete()


# Функция для удаления кубиков сообщений с задержкой
async def delete_two_messages(msg1, msg2, delay=30):
    await asyncio.sleep(delay)
    await msg1.delete()
    await msg2.delete()


# /dice
async def send_dice(message: types.Message):
    await message.delete()
    current_date = datetime.datetime.now().date()
    user_id = message.from_user.id
    user_name = message.from_user.mention
    full_name = message.from_user.full_name
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

                await message.answer(
                    f"{full_name}\n\nПобеда {game_info}\n\nВсего бросков: {all_count}\nВыигрышных бросков: {win_count}")

                await increment_user_count_win(user_id)
                await get_user_coupons(message)

            else:

                await write_user_last_time(user_id, current_date, user_name, full_name)
                game_info = status[game_over - 1][game_over]
                await asyncio.sleep(3.70)

                all_count, win_count = await user_count_dice_win_and_alldice(user_id)
                await zarik_money(message, game_over, user_id, game_info, full_name, game_over, all_count,
                                  win_count)

                await asyncio.create_task(delete_two_messages(bot_data1, bot_data2, 30))
        else:
            msg = await message.answer("Вы уже бросили кубики сегодня. Попробуйте завтра!")
            await asyncio.sleep(10)
            await msg.delete()
    except:
        pass


async def zarik_money(message: types.Message, money, user_id, game_info, full_name, game_over, all_count, win_count):
    connection, cursor = connect_data_b()
    cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
    row = cursor.fetchone()

    if row is not None:
        cursor.execute("UPDATE users SET money = money + %s WHERE user_id = %s", (money, user_id,))

        # Асинхронно отправляем сообщение и устанавливаем таймер на его удаление
        asyncio.create_task(send_and_delete_message(message,
                                                    f"{game_info}\n\n*{full_name}* Вы проиграли!\n\nВам начислены коины:"
                                                    f" {game_over}\n\nНе забудьте делиться с другими участниками монетами: "
                                                    f"ответом на сообщение пользователя"
                                                    f" `/send {game_over}`\n\nВсего бросков: "
                                                    f"{all_count}\nВыигрышных бросков: {win_count}",
                                                    29))
    else:
        asyncio.create_task(send_and_delete_message(message,
                                                    'Вы не найдены в базе магазина, коины не будут начислены,'
                                                    ' примите правила магазина! *@KRAFT_STORE_BOT*', 30))

    cursor.close()
    connection.close()


# /dice_info X

async def dice_info(message: types.Message):
    param = message.get_args()
    await message.delete()
    if param == 'list':
        asyncio.create_task(dice_rol_list(message))
    elif param == "win":
        asyncio.create_task(dice_rol_list_win(message))
    else:
        msg = await message.answer("Работает только с параметрами `win/list` `/dice_info list`", parse_mode='markdown')

        await asyncio.sleep(20)
        await msg.delete()
