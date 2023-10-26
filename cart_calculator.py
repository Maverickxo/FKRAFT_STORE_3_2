from cart_utils import clear_user_cart, get_cart_items
from add_coopon import *
from card_list import *
from allert_info import *
from add_price import *
from change_price import *
from change_status import *

from aiogram import types

from user_money_to_cart import calc_money_cart
from datetime import datetime, timedelta

from delivery_method import mode_of_delivery

conn = sqlite3.connect("ShopDB.db")
cursor = conn.cursor()


def get_dt():
    current_dt = datetime.now()
    new_dt = current_dt + timedelta(hours=3)
    format_dt = new_dt.strftime("%d-%m-%Y %H:%M:%S")
    return format_dt


async def calculate_delivery_cost(product_price, delivery_cost):
    delivery_increase = (product_price - 5000) // 5000

    if delivery_increase > 0:
        increased_cost = delivery_increase * 100
        delivery_cost += increased_cost
    else:
        increased_cost = 0

    return delivery_cost, increased_cost


async def order_informer(random_number_order, total_price1, delivery, coupon, order_user, user_id):
    await bot.send_message(-1001683359105, f"Оформлен заказ №{random_number_order}\n"
                                           f"Сумма к оплате: {total_price1} руб.\n"
                                           f"Отправка: {delivery}\n"
                                           f"Купон: {coupon}\n\n"
                                           f"Клиент: {order_user} `/ban {user_id}`", parse_mode='markdown')



class OrderForm(StatesGroup):
    COUPON = State()  # Состояние ввода купона


async def process_enter_coupon(message: types.Message, state: FSMContext):
    order_user = message.from_user.full_name
    coupon = message.text
    chat_id = message.chat.id
    formatted_datetime = get_dt()
    async with state.proxy() as data:
        money_value = data.get("money_value", 0)  # Получаем значение money_value из данных состояния.
        delivery_method = data["delivery_method"]
        user_id = message.from_user.id
        random_number_order = random.randint(100000, 999999)
        cart_items = get_cart_items(user_id)
        cart_text = f"Заказ в интернет-магазине KRAFT №{random_number_order} \n\nСодержимое корзины со скидкой:\n"
        total_price = 0
        discount_amount = 0

        try:
            cursor.execute("SELECT * FROM coupons WHERE coupon_code = ?", (coupon,))
            result = cursor.fetchone()
            if result is not None:
                await types.ChatActions.typing()
                discount_percentage = result[2]
                for item in cart_items:
                    product = item["product"]
                    quantity = item["quantity"]
                    price = product[2] * quantity
                    cart_text += f"- {product[1]} ({product[2]} руб.) x {quantity} = {price} руб.\n"
                    total_price += price

                discount_amount = int(total_price * (discount_percentage / 100))
                total_amount = int(total_price - discount_amount)

                if result[3] == 0:
                    cursor.execute("DELETE FROM coupons WHERE coupon_code = ?", (coupon,))
                conn.commit()

                await bot.send_message(chat_id, "Купон Применен.")
            else:
                buttons = [
                    types.InlineKeyboardButton(
                        "Вести еще раз", callback_data="coupon_yes"
                    ),
                    types.InlineKeyboardButton(
                        "Продолжить без купона", callback_data="coupon_no"
                    ),
                ]
                keyboard = types.InlineKeyboardMarkup(row_width=2)
                keyboard.add(*buttons)
                await bot.send_message(
                    chat_id, "Купон не найден.", reply_markup=keyboard
                )
                return  # Возвращаемся, не выполняя расчет корзины

        except sqlite3.Error as e:
            print("Ошибка работы с базой данных:", e)
            delivery_value = 0

        # Блок расчета корзины только в случае успешного применения купона
        delivery_options = {
            "Экспресс": 1200,
            "Экспресс + страховка": 1300,
            "Обычная": 600,
            "Обычная + страховка": 700,
        }
        delivery = delivery_options.get(delivery_method, "")
        if delivery:
            delivery_value = delivery_options[delivery_method]

            delivery_value, delivery = mode_of_delivery(delivery_method)

        total_price1 = total_price + delivery_value

        cart_text += (
            f"\nПодытог: {total_price} руб. + {delivery} >> Итого = {total_price1} руб."
        )
        total_cost, increased_delivery = await calculate_delivery_cost(total_price, delivery_value)

        total_amount1 = total_amount + delivery_value

        primstoim = increased_delivery + total_amount1

        cart_data = calc_money_cart(money_value, primstoim, user_id)
        primstoim -= money_value

        random_number = random.choice(numbers_cards)
        digits = random_number[:19]
        remaining_text = random_number[20:]

        if primstoim <= 0:
            primstoim = "❗️ОПЛАЧЕНО❗️"
        await bot.send_message(
            user_id,
            f"{cart_text}\n\n"
            "Информация о заказе:\n"
            "\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\n"
            f"Дата заказа: {formatted_datetime}(MSK)\n"
            f"ФИО: {data['fio']}\n"
            f"Индекс: {data['index']}\n"
            f"Город: {data['city']}\n"
            f"Улица: {data['street']}\n"
            f"Номер дома и квартиры: {data['house']}\n"
            "\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\n\n"
            f"Купон: {coupon}\n"
            f"Процент скидки: {discount_percentage} %.\n"
            f"Сумма скидки: {discount_amount} руб.\n"
            f"После применения купона : {total_amount} руб.\n\n"

            f"{cart_data}\n"

            f"Стоимость доставки увеличилась на: {increased_delivery} руб.\n"
            f"Итоговая стоимость доставки: {total_cost} руб.\n\n"

            "Реквизиты для оплаты:\n"
            "--------------------------------------------\n"
            f"`{digits}` {remaining_text}\n"
            "--------------------------------------------\n"
            f"Сумма к оплате: {primstoim} руб.\n", parse_mode='markdown')

        coupon = f"{coupon} - {discount_percentage}%"
        await alert_hd(message)
        clear_user_cart(user_id)

        # await order_informer(random_number_order, primstoim, delivery, coupon, order_user)
    await state.finish()


async def process_coupon_inline_callback(query: types.CallbackQuery, state: FSMContext):
    order_user = query.from_user.full_name
    formatted_datetime = get_dt()
    chat_id = query.message.chat.id
    callback_data = query.data
    if callback_data == "coupon_yes":
        await bot.send_message(chat_id, "Введите купон:")
        await OrderForm.COUPON.set()
    elif callback_data == "coupon_no":
        await bot.send_message(chat_id, "Продолжаем без купона...")
        async with state.proxy() as data:
            money_value = data.get("money_value", 0)  # Получаем значение money_value из данных состояния.
            delivery_method = data["delivery_method"]

        async with state.proxy() as data:
            user_id = query.from_user.id
            random_number_order = random.randint(100000, 999999)
            cart_items = get_cart_items(user_id)
            cart_text = f"Заказ в интернет-магазине KRAFT №{random_number_order} \n\nСодержимое корзины:\n"
            total_price = 0
            for item in cart_items:
                product = item["product"]
                quantity = item["quantity"]
                price = product[2] * quantity
                cart_text += f"- {product[1]} ({product[2]} руб.) x {quantity} = {price} руб.\n"
                total_price += price
                total_price1 = total_price
                delivery_value = 0

                delivery_value, delivery = mode_of_delivery(delivery_method)

            #

            if total_price >= 130000:
                discount = total_price * 0.15
                total_price -= discount
                total_price1 = delivery_value + total_price
                total_price1 = int(total_price1)  # Округляем до целого числа
                cart_text += f"\nПодытог: {int(total_price)} руб. (со скидкой на опт) + {delivery} >> Итого = {total_price1} руб."
            else:
                total_price1 = delivery_value + total_price
                total_price1 = int(total_price1)  # Округляем до целого числа
                cart_text += f"\nПодытог: {int(total_price)} руб. + {delivery} >> Итого = {total_price1} руб."

            random_number = random.choice(numbers_cards)
            digits = random_number[:19]
            remaining_text = random_number[20:]

            total_cost, increased_delivery = await calculate_delivery_cost(int(total_price), int(delivery_value))

            final_price = increased_delivery + total_price1

            cart_data = calc_money_cart(money_value, final_price, user_id)
            final_price -= money_value

            if final_price <= 0:
                final_price = "❗️ОПЛАЧЕНО❗️"
            await bot.send_message(
                user_id,
                f"{cart_text}\n\n"
                f"Информация о заказе:\n"
                "\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\n"
                f"Дата заказа: {formatted_datetime}(MSK)\n"
                f"ФИО: {data['fio']}\n"
                f"Индекс: {data['index']}\n"
                f"Город: {data['city']}\n"
                f"Улица: {data['street']}\n"
                f"Номер дома и квартиры: {data['house']}\n"
                "\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\n\n"

                f"Стоимость доставки увеличилась на: {increased_delivery} руб.\n"
                f"Итоговая стоимость доставки: {total_cost} руб.\n\n"

                f"{cart_data}\n\n"
                f"Реквизиты для оплаты:\n"
                "--------------------------------------------\n"
                f"`{digits}` {remaining_text}\n"
                "--------------------------------------------\n"
                f"Сумма к оплате: {final_price} руб.\n", parse_mode='markdown')
            coupon = "Без купона"
            await alert_hd(query.message)
            clear_user_cart(user_id)
            # await order_informer(random_number_order, final_price, delivery, coupon, order_user)
        await state.finish()
