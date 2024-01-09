carts = {}


async def add_delivery_cost(total_price, delivery_value):
    if total_price < 4500:
        add_total_p = 600
        delivery_cost = delivery_value + 600
        add_cost_dely = (f"❗️Сумма минимального заказа меньше 4500р.❗️\n"
                         f"❗️Стоимость доставки увеличена на 600р.❗️\n\n"
                         f"Итоговая стоимость доставки: {delivery_cost} руб.\n\n")

    else:
        add_cost_dely = ''
        add_total_p = 0

    return add_cost_dely, add_total_p


async def calculate_delivery_cost(product_price, delivery_cost):
    # delivery_increase = 0  # TODO отключить 1 января

    delivery_increase = (product_price - 5000) // 5000
    if delivery_increase > 0:
        increased_cost = delivery_increase * 100
        delivery_cost += increased_cost
        info_delivery = (f"Стоимость доставки увеличилась на: {increased_cost} руб.\n"
                         f"Итоговая стоимость доставки: {delivery_cost} руб.\n\n")
    else:
        increased_cost = 0
        info_delivery = ''

    return delivery_cost, increased_cost, info_delivery


def add_to_cart(user_id, product):
    if user_id not in carts:
        carts[user_id] = []
    cart = carts[user_id]
    for item in cart:
        if item["product"] == product:
            item["quantity"] += 1
            return
    cart.append({"product": product, "quantity": 1})


def get_cart_items(user_id):
    if user_id in carts:
        return carts[user_id]
    return []


def clear_user_cart(user_id):
    if user_id in carts:
        del carts[user_id]


def remove_from_cart(user_id, product):
    if user_id in carts:
        cart = carts[user_id]
        for item in cart:
            if item["product"] == product:
                item["quantity"] -= 1
                if item["quantity"] == 0:
                    cart.remove(item)
                return


def get_product_quantity(user_id, product):
    cart_items = get_cart_items(user_id)
    for item in cart_items:
        if item["product"] == product:
            return item["quantity"]
    return 0
