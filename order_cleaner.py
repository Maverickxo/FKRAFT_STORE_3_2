from connect_bd import connect_data_b
from datetime import datetime, timedelta
from StoreBOT import bot


async def non_pay_orders(message_id, message_chat_id, order_zakaz):
    connection, cursor = connect_data_b()
    data_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    cursor.execute(
        'INSERT INTO non_pay_orders (message_id, message_chat_id, order_zakaz, data_time) VALUES (%s, %s, %s, %s)',
        (message_id, message_chat_id, order_zakaz, data_time,))

    cursor.close()
    connection.close()


async def check_time_order():
    connection, cursor = connect_data_b()
    current_time = datetime.now()
    time_threshold = current_time - timedelta(hours=24)
    cursor.execute("SELECT * FROM non_pay_orders WHERE to_timestamp(data_time, 'DD-MM-YYYY HH24:MI:SS') <= %s",
                   (time_threshold,))
    results = cursor.fetchall()
    for row in results:
        print(f'{row[1]} {row[2]}')
        chat_id = row[2]
        message_id = row[1]
        order_zakaz = row[3]
        try:
            await bot.delete_message(chat_id, message_id)
            print(f"Сообщение в чате {row[2]}, с идентификатором {row[1]} успешно удалено.")
            cursor.execute('DELETE FROM non_pay_orders WHERE order_zakaz = %s', (order_zakaz,))
            print('Заказ удален из базы')
        except Exception as e:
            print(f"Ошибка удаления сообщения: {e}")
    cursor.close()
    connection.close()
