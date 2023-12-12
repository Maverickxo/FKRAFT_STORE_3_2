from connect_bd import connect_data_b


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


def money_ostatok_func(amount, user_id):  # TODO готов
    connection, cursor = connect_data_b()
    cursor.execute("UPDATE users SET money = money + %s WHERE user_id = %s ", (amount, user_id))
    cursor.close()
    connection.close()
