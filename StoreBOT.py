import logging
import sqlite3
import types

from cart_utils import clear_user_cart, get_cart_items, add_to_cart, remove_from_cart, get_product_quantity

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types.web_app_info import WebAppInfo

from help_msg import help_user
from check_access import *
from print_coopon import *
from check_coopon import *
from add_coopon import *
from admin_commands import *

from balans_user import *

from allert_info import *
from support import *
from block_list import *
from speak_user import *
import check_exists_db
from add_price import *
from change_price import *
from change_status import *
from del_price import del_price, delete_product
from cart_calculator import process_enter_coupon, process_coupon_inline_callback

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
user_db = Database("ShopDB.db")
conn = sqlite3.connect("ShopDB.db")
cursor = conn.cursor()

logging.basicConfig(level=logging.INFO)

technical_works = False


class OrderForm(StatesGroup):
    FIO = State()  # Состояние ФИО
    INDEX = State()  # Состояние индекса
    CITY = State()  # Состояние города
    STREET = State()  # Состояние улицы
    HOUSE = State()  # Состояние номера дома
    DELIVERY = State()  # Состояние доставки
    COUPON = State()  # Состояние ввода купона
    EDIT_PRICE = State()
    NEW_PRICE = State()
    PRODUCT_ACTIVE = State()
    PRODUCT_NAME = State()
    WAIT_FOR_MONEY = State()


async def check_technical_works(message):
    global technical_works
    if not technical_works:
        await message.answer("⚠️ В магазине ведутся технические работы ⚠️")
        return


def get_products_from_db():
    products_list = sqlite3.connect('ShopDB.db')
    return products_list.execute("SELECT * FROM products WHERE active = 1 ").fetchall()


async def start_command(message: types.Message):
    global technical_works
    if not technical_works:
        await message.answer("⚠️В магазине ведутся тех работы⚠️")
    else:
        products = get_products_from_db()
        if len(products) == 0:
            msg = await message.answer(
                "⚠️В магазине не добавлены товары⚠️\nдля добавления товара используйте |`/add_product`|",
                parse_mode='markdown')

        else:
            products = [{'name': p[1], 'price': p[2]} for p in products]

            user_id = message.from_user.id
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            for product in products:
                button_text = f"{product['name']} - {product['price']} руб."
                quantity = get_product_quantity(user_id, product)
                if quantity > 0:
                    button_text += f" ({quantity} шт.)"
                button = types.InlineKeyboardButton(
                    button_text, callback_data=f"add_to_cart_{product['name']}"
                )
                keyboard.add(button)
            cart_button = types.InlineKeyboardButton("Корзина", callback_data="show_cart")
            clear_button = types.InlineKeyboardButton(
                "Очистить корзину", callback_data="clear_cart"
            )
            keyboard.add(cart_button, clear_button)
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(
                # types.KeyboardButton('Образец зaказа', web_app=WebAppInfo(
                # url='https://maverickxo.github.io/kraftstore.github.io/sample_order.html')),
                types.KeyboardButton(
                    "Магазин",
                    web_app=WebAppInfo(
                        url="https://maverickxo.github.io/kraftstore.github.io/"
                    ),
                ),
                types.KeyboardButton(
                    "Отзывы",
                    web_app=WebAppInfo(
                        url="https://maverickxo.github.io/kraftstore.github.io/reviews.html"
                    ),
                ),
            )
            await message.answer("🛒 Добро пожаловать в магазин KRAFT! 🛍️", reply_markup=markup)
            await message.answer("Выберите товар:", reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data.startswith("add_to_cart_"))
async def handle_button_click(callback_query: types.CallbackQuery):
    global technical_works
    if not technical_works:
        await callback_query.answer("⚠️В магазине ведутся тех работы⚠️")
    else:

        products = get_products_from_db()

        user_id = callback_query.from_user.id
        if user_db.check_ban_status(user_id):
            await callback_query.answer(BAN_MSG)
        else:
            await callback_query.answer()
            product_name = callback_query.data.split("_")[-1]
            selected_product = next((p for p in products if p[1] == product_name), None)

            if selected_product:
                user_id = callback_query.from_user.id
                add_to_cart(user_id, selected_product)
                await update_button_text(callback_query.message, user_id)


@dp.callback_query_handler(lambda c: c.data == "show_cart")
async def show_cart(callback_query: types.CallbackQuery):
    global technical_works
    if not technical_works:
        await callback_query.answer("⚠️В магазине ведутся тех работы⚠️")
    else:

        user_id = callback_query.from_user.id
        if user_db.check_ban_status(user_id):
            await callback_query.answer(BAN_MSG)
        else:
            cart_items = get_cart_items(user_id)
            if cart_items:
                cart_text = "Содержимое вашей корзины:\n"
                total_price = 0
                for item in cart_items:
                    product = item["product"]
                    quantity = item["quantity"]

                    price = product[2] * quantity
                    cart_text += f"- {product[1]} ({product[2]} руб.) x {quantity} = {price} руб.\n"
                    total_price += price
                cart_text += f"\nИтого: {total_price} руб."

                if total_price < 4500:
                    keyboard = types.InlineKeyboardMarkup()
                    clear_button = types.InlineKeyboardButton(
                        "Очистить корзину", callback_data="clear_cart"
                    )
                    keyboard.add(clear_button)
                    await bot.send_message(
                        user_id,
                        f"Минимальная сумма заказа: 4500руб. Ваш заказ: {total_price}руб.",
                        reply_markup=keyboard,
                    )
                    return

                keyboard = types.InlineKeyboardMarkup()
                clear_button = types.InlineKeyboardButton(
                    "Очистить корзину", callback_data="clear_cart"
                )
                buy_button = types.InlineKeyboardButton("Купить", callback_data="buy")
                keyboard.add(clear_button, buy_button)
            else:
                cart_text = "Ваша корзина пуста"
                keyboard = None
            await bot.send_message(user_id, cart_text, reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data == "clear_cart")
async def clear_cart(callback_query: types.CallbackQuery):
    global technical_works
    if not technical_works:
        await callback_query.answer("⚠️В магазине ведутся тех работы⚠️")
    else:
        user_id = callback_query.from_user.id
        if user_db.check_ban_status(user_id):
            await callback_query.answer(BAN_MSG)
        else:
            try:
                clear_user_cart(user_id)
                total_price1 = 0
                msg = await bot.send_message(user_id, "Корзина очищена")
                await update_button_text(callback_query.message, user_id)
                await asyncio.sleep(5)
                await msg.delete()
            except:
                pass


async def update_button_text(message, user_id):
    products = get_products_from_db()
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    for product in products:
        button_text = f"{product[1]} - {product[2]} руб."  # Обращение к элементам по индексам
        quantity = get_product_quantity(user_id, product)
        if quantity > 0:
            button_text += f" ({quantity} шт.)"
            decrease_button = types.InlineKeyboardButton(
                "❌ уменьшить кол-во. ❌",
                callback_data=f"decrease_quantity_{product[1]}",  # Обращение к названию по индексу
            )
            keyboard.add(decrease_button)
        button = types.InlineKeyboardButton(
            button_text, callback_data=f"add_to_cart_{product[1]}"  # Обращение к названию по индексу
        )
        keyboard.add(button)
    cart_button = types.InlineKeyboardButton("Корзина", callback_data="show_cart")
    clear_button = types.InlineKeyboardButton(
        "Очистить корзину", callback_data="clear_cart"
    )
    keyboard.add(cart_button, clear_button)
    await bot.edit_message_reply_markup(
        chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard
    )


@dp.callback_query_handler(lambda c: c.data.startswith("decrease_quantity_"))
async def decrease_quantity(callback_query: types.CallbackQuery):
    global technical_works
    if not technical_works:
        await callback_query.answer("⚠️В магазине ведутся тех работы⚠️")
    else:
        products = get_products_from_db()
        product_name = callback_query.data.split("_")[-1]
        selected_product = next((p for p in products if p[1] == product_name), None)

        if selected_product:
            user_id = callback_query.from_user.id
            remove_from_cart(user_id, selected_product)
            await update_button_text(callback_query.message, user_id)


@dp.callback_query_handler(lambda c: c.data == "buy")
async def buy_product(callback_query: types.CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    money_value = await get_money_value_from_db(user_id)
    global technical_works
    if not technical_works:
        await callback_query.answer("⚠️В магазине ведутся тех работы⚠️")
    else:
        user_id = callback_query.from_user.id
        cart_items = get_cart_items(user_id)

        total_price = sum(item["product"][2] * item["quantity"] for item in cart_items)
        if total_price < 4500:
            keyboard = types.InlineKeyboardMarkup()
            clear_button = types.InlineKeyboardButton(
                "Очистить корзину", callback_data="clear_cart"
            )
            keyboard.add(clear_button)
            await bot.send_message(
                user_id,
                f"Самый умный ?! Минимальная сумма заказа: 4500руб. Ваш заказ: {total_price}руб.",
                reply_markup=keyboard,
            )
            return
        await callback_query.answer()

        if money_value > 0:
            # Если значение money больше 0, показываем инлайн-кнопки.
            await state.update_data(money_value=money_value)  # Сохраняем money_value в состоянии.

            keyboard = InlineKeyboardMarkup()
            yes_button = InlineKeyboardButton("Да", callback_data="use_money_yes")
            no_button = InlineKeyboardButton("Нет", callback_data="use_money_no")
            keyboard.add(yes_button, no_button)

            await callback_query.message.answer(f"У вас есть деньги на счету ({money_value}). Желаете использовать их?",
                                                reply_markup=keyboard)
            await OrderForm.WAIT_FOR_MONEY.set()  # Переходим на новое состояние.
        else:

            await OrderForm.FIO.set()
            await bot.send_message(callback_query.from_user.id, "Введите ваше ФИО:")


@dp.callback_query_handler(state=OrderForm.WAIT_FOR_MONEY)
async def process_money_response(callback_query: CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    async with state.proxy() as data:
        if callback_query.data == "use_money_yes":
            data["money_used"] = True
            money_value = data.get("money_value", 0)
            await callback_query.message.answer(f"Используем деньги на счету: {money_value}")
            await set_money_to_zero(user_id)
        else:
            data["money_used"] = False
            data["money_value"] = 0  # Обнуляем значение money_value

        await OrderForm.FIO.set()
        await callback_query.message.answer("Введите ваше ФИО:")


@dp.message_handler(state=OrderForm.FIO)
async def process_fio(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["fio"] = message.text

        await OrderForm.INDEX.set()
        await message.answer("Введите ваш индекс:")


@dp.message_handler(state=OrderForm.INDEX)
async def process_index(message: types.Message, state: FSMContext):
    index = message.text.strip()
    if not index.isdigit() or len(index) != 6:
        await message.answer("Некорректный индекс. Пожалуйста, введите 6 цифр.")
        return

    async with state.proxy() as data:
        data["index"] = index
    await OrderForm.CITY.set()
    await message.answer("Введите ваш населенный пункт:")


@dp.message_handler(state=OrderForm.CITY)
async def process_city(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["city"] = message.text

    await OrderForm.STREET.set()
    await message.answer("Введите вашу улицу:")


@dp.message_handler(state=OrderForm.STREET)
async def process_street(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["street"] = message.text

    await OrderForm.HOUSE.set()
    await message.answer("Введите номер вашего дома и квартиры:")


@dp.message_handler(state=OrderForm.HOUSE)
async def process_house(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["house"] = message.text

    delivery_methods = [
        {"name": "Обычная", "price": 600},
        {"name": "Обычная + страховка", "price": 700},
        {"name": "Экспресс", "price": 1200},
        {"name": "Экспресс + страховка", "price": 1300},
    ]

    keyboard = types.InlineKeyboardMarkup(row_width=2)
    for method in delivery_methods:
        button_text = f"{method['name']} - {method['price']} руб."
        button = types.InlineKeyboardButton(
            button_text, callback_data=f"select_delivery_{method['name']}"
        )
        keyboard.add(button)
    await bot.send_message(
        message.from_user.id, "Выберите способ отправки:", reply_markup=keyboard
    )
    await OrderForm.DELIVERY.set()


@dp.callback_query_handler(
    lambda c: c.data.startswith("select_delivery_"), state=OrderForm.DELIVERY
)
async def select_delivery_method(callback_query: CallbackQuery, state: FSMContext):
    delivery_method = callback_query.data.replace("select_delivery_", "")
    async with state.proxy() as data:
        data["delivery_method"] = delivery_method
    await bot.send_message(
        callback_query.from_user.id, f"Вы выбрали способ отправки: {delivery_method}."
    )
    buttons = [
        types.InlineKeyboardButton("Да, есть купон", callback_data="coupon_yes"),
        types.InlineKeyboardButton("Нет, продолжить", callback_data="coupon_no"),
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    await bot.send_message(
        callback_query.from_user.id, "У вас есть купон?", reply_markup=keyboard
    )
    await OrderForm.COUPON.set()


@dp.message_handler(commands=["reset"], state="*")
@aut_cgt()
async def reset_state(message: types.Message, state: FSMContext):
    await state.reset_state()
    user_id = message.from_user.id
    clear_user_cart(user_id)
    await message.answer("Заказ сброшен. Вы можете начать новый заказ.")


@dp.message_handler(commands=["start"])
@aut_cgt()
@check_ban_status
async def help_command(message: types.Message):
    user_id = message.from_user.id
    money_value = await get_money_value_from_db(user_id)
    global technical_works
    if not technical_works:
        await message.answer("⚠️В магазине ведутся тех работы⚠️")
    else:
        btn_yes = types.InlineKeyboardButton(text="Ознакомлен", callback_data="rules_yes")
        btn_no = types.InlineKeyboardButton(text="Отказ", callback_data="rules_no")
        btn_help = types.InlineKeyboardButton(text="Инструкция", callback_data="rules_help")

        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(btn_yes, btn_no, btn_help)
        msg = await message.answer(f"Приветствую {message.from_user.full_name}❗️\n\n"
                                   f"Твой баланс: {money_value} KRAFT coins\n"
                                   f"Узнать свой баланс: /get_balance\n\n"
                                   f"Для получения доп. информации\nоб использовании "
                                   f"и накоплении KRAFT coins\nобратитесь к администраторам:\n\n"
                                   f"@blockmor\n@Maver1ckxo\n@ZalehvatSky")

        await asyncio.sleep(10)
        await msg.delete()
        await message.delete()
        await message.answer(
            f"Правила магазина KRAFT:\n{TEXT_RULES}", reply_markup=keyboard
        )

        if not user_db.user_exists(message.from_user.id):
            if message.from_user.last_name is not None:
                full_name = escape_markdown(f"{message.from_user.first_name} {message.from_user.last_name}")
            else:
                full_name = escape_markdown(message.from_user.first_name)
            user_db.add_user(message.from_user.id, full_name)


@dp.callback_query_handler(text_contains="rules")
async def rules(call: types.CallbackQuery):
    if call.data == "rules_yes":
        await start_command(call.message)
        await call.message.delete()
    elif call.data == "rules_help":
        await help_user(call.message)
        await call.message.delete()
    elif call.data == "rules_no":
        user_db.user_ban(call.from_user.id)
        await call.message.delete()
        await call.message.answer("Вы заблокированы!")
    elif call.data == "rules_back":
        await help_command(call.message)
        await call.message.delete()
    elif call.data == "rules_dumb":
        await dumb_msg(call.message)


@dp.message_handler(commands=["speak_store"])
@auth
async def speak(message: types.Message):
    await speak_user(message)


@dp.message_handler(commands=["users_count"])
@auth
async def usr_count(message: types.Message):
    user_count = user_db.user_count()
    msg = await message.answer(f"Подписчиков в боте: {user_count}", parse_mode="markdown")
    await asyncio.sleep(5)
    await message.delete()
    await msg.delete()


@dp.message_handler(commands=["help"])
@aut_cgt()
@check_ban_status
async def help_nb(message: types.Message):
    global technical_works
    if not technical_works:
        await message.answer("⚠️В магазине ведутся тех работы⚠️")
    else:
        await message.answer(HELP, parse_mode="markdown")


@dp.message_handler(commands=["weekend_coupons"])
@auth
async def handle_coupons_by(message: types.Message):
    await weekend_coupons(message)


@dp.message_handler(commands=["adm_get_coupons"])
@auth
async def handle_print_coupons(message: types.Message):
    await print_coupons(message)


@dp.message_handler(commands=["ck_coupon"])
async def handle_check_coupon(message: types.Message):
    await check_coupon(message)


@dp.message_handler(commands=["add_coupon_pack"])
@auth
async def handle_add_coupon_pack(message: types.Message):
    await add_coupon_pack(message)


@dp.message_handler(commands=["list_coupon_of_time"])
@auth
async def handle_print_off_time_coupon(message: types.Message):
    await print_coupons_off_time(message)


@dp.message_handler(commands=["add_coupon"])
@auth
async def handle_add_coupon(message: types.Message):
    await add_coupon(message)


@dp.message_handler(commands=["add_coupon_off_time"])
@auth
async def handle_add_coupon_off_time(message: types.Message):
    await add_coupon_off_time(message)


@dp.message_handler(commands=["del_coupon_off_time"])
async def delete_coupon_code_handler(message: types.Message):
    await delete_coupon_by_code(message)


@dp.message_handler(commands=["adm_help"])
@auth
async def handle_help_adm_command(message: types.Message):
    await handle_help_adm(message)


@dp.message_handler(commands=["response_storeBot"])
@auth
async def res_qu(message: types.Message):
    await send_response(message)


@dp.message_handler(commands=["question"])
@aut_cgt()
@check_ban_status
async def ques_send(message: types.Message):
    await send_qwests(message)


@dp.message_handler(commands=["block_list"])
@auth
async def ban_list(message: types.Message):
    await usr_count_ban(message)


@dp.message_handler(commands=["user_list"])
@auth
async def ban_list(message: types.Message):
    await usr_list(message)


@dp.message_handler(commands=["unban"])
@auth
async def usr_unban(message: types.Message):
    await unban_user(message)


@dp.message_handler(commands=["products_to_delete"])
@auth
async def del_price_handler(message: types.Message):
    await del_price(message)


@dp.message_handler(commands=["ban"])
@auth
async def usr_ban(message: types.Message):
    await ban_user(message)


@dp.message_handler(commands=["toggle_product"])
@auth
async def activ_product(message: types.Message):
    await product_list(message)


@dp.message_handler(commands=["edit_product_price"])
@auth
async def activ_product_price(message: types.Message):
    await product_list_edit_price(message)


@dp.message_handler(commands=['add_product'])
async def add_product_handler(message: types.Message):
    await message.answer("Введите название товара:")
    await OrderForm.PRODUCT_NAME.set()


@dp.message_handler(commands=["del"])
@auth
async def delete_product_handler(message: types.Message):
    await delete_product(message)


@dp.message_handler(commands=["about"])
@auth
async def about_handler(message: types.Message):
    await message.answer(f"{INFO}", parse_mode='Markdown')


@dp.message_handler(commands=["technical_works"])
@auth
async def technical_works(message: types.Message):
    global technical_works
    technical_works = not technical_works
    await message.answer("✅Технические работы выключены✅" if technical_works else "⚠️Технические работы включены⚠️")


@dp.message_handler(commands=["get_balance"])
@aut_cgt()
@check_ban_status
async def technical_works(message: types.Message):
    user_id = message.from_user.id
    money_value = await get_money_value_from_db(user_id)
    await message.delete()
    msg = await message.answer(f"Ваш баланс: {money_value} KRAFT coins")
    await asyncio.sleep(10)
    await msg.delete()


@dp.message_handler(commands=["get_user_balance"])
@auth
async def user_balans_handler(message: types.Message):
    await usr_balans_list(message)


@dp.message_handler(commands=["add_user_balance"])
@auth
async def user_add_balans_handler(message: types.Message):
    await add_user_balance_list(message)


@dp.message_handler(commands=['deposit'])
@auth
async def add_deposit_user(message: types.Message):
    await add_deposit(message)
    try:
        await message.delete()
        await message.delete()
    except aiogram.exceptions.BadRequest:
        pass


@dp.message_handler(commands=['checkbalance'])
@auth
async def check_user_money_handler(message: types.Message):
    await check_user_money(message)

from dice_rol import send_dice
@dp.message_handler(commands=['dice'])
@aut_cgt()
@check_ban_status
async def dice_rol_handler(message: types.Message):
    await send_dice(message)

dp.register_callback_query_handler(process_coupon_inline_callback, lambda query: query.data.startswith("coupon_"),
                                   state=OrderForm.COUPON)

dp.register_message_handler(process_enter_coupon, state=OrderForm.COUPON)

dp.register_callback_query_handler(change_product_status, lambda c: c.data.startswith("change_status_"))

dp.register_callback_query_handler(change_price, lambda c: c.data.startswith('change_price_'))

dp.register_message_handler(handle_new_price, state=OrderForm.EDIT_PRICE)

dp.register_message_handler(enter_product_name_handler, state=OrderForm.PRODUCT_NAME)

dp.register_message_handler(enter_product_price_handler, state=OrderForm.NEW_PRICE)

dp.register_message_handler(enter_product_active_handler, state=OrderForm.PRODUCT_ACTIVE)

if __name__ == "__main__":
    from aiogram import executor

    current_datetime = datetime.datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

    print(formatted_datetime)
    '''Перед первым запуском раскомментировать '''
    # check_exists_db.create_database_and_tables()
    # check_exists_db.check_database_and_tables()
    '''----------------------------------------'''
    executor.start_polling(dp, skip_updates=True)
