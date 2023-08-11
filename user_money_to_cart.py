import sqlite3


def calc_money_cart(money_value, total_amount1, user_id):
    money_user = money_value

    if money_value > 0:
        rem_money = 0
        money_ostatok = 0
        used_money = min(money_value, total_amount1)  # Используем минимум из money_value и total_amount1
        money_ostatok = money_user - used_money
        rem_money = total_amount1 - used_money
        cart_data = (f'Использовано KRAFT coins: {used_money}\n'
                     f'Итоговая сумма: {total_amount1} - {used_money} = {rem_money} руб.\n'
                     f'Остаток KRAFT coins: {money_ostatok}\n')
        money_ostatok_func(money_ostatok, user_id)
    else:
        cart_data = f'Использовано KRAFT coins: {money_value}\n'
    return cart_data



def money_ostatok_func(amount, user_id):
    conn = sqlite3.connect('ShopDB.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET money = money + ? WHERE user_id = ?", (amount, user_id))
    conn.commit()
    conn.close()


# user_id = 5869013585
# money = 1500
# total_price = 6000
# print(calc_money_cart(money, total_price, user_id))
