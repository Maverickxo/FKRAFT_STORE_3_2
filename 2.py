def generate_cart_text(total_price, delivery_value, delivery):
    if total_price >= 130000:
        discount = total_price * 0.15
        total_price -= discount
        total_price1 = delivery_value + total_price
        total_price1 = int(total_price1)
        cart_text = f"\nПодытог: {int(total_price)} руб. (со скидкой на опт) + {delivery} >> Итого = {total_price1} руб."
    else:
        total_price1 = delivery_value + total_price
        total_price1 = int(total_price1)
        cart_text = f"\nПодытог: {int(total_price)} руб. + {delivery} >> Итого = {total_price1} руб."

    return cart_text


# Пример использования функции
total_price = 140000
delivery_value = 600
delivery = "Обычная"

cart_text = generate_cart_text(total_price, delivery_value, delivery)
print(cart_text)
