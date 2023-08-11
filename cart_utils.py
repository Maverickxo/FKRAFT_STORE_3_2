carts = {}


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
