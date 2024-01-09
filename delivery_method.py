def mode_of_delivery(delivery_method):
    if delivery_method == "Экспресс":
        delivery = "‼️Экспресс: 1200р.‼️"
        delivery_value = 1200

    elif delivery_method == "Экспресс + страховка":
        delivery = "‼️Экспресс + ✅страховка✅: 1300р.‼️"
        delivery_value = 1300

    elif delivery_method == "Обычная":
        delivery_value = 600
        delivery = "Обычная: 600р."

    elif delivery_method == "Обычная + страховка":
        delivery_value = 700
        delivery = "Обычная + ✅страховка✅: 700р."

    elif delivery_method == "Santa Claus delivery":
        delivery_value = 1
        delivery = "Santa Claus delivery: 1р."

    return delivery_value, delivery
