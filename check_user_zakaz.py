from connect_bd import connect_data_b
from aiogram import types
from StoreBOT import bot


async def check_user_zakazz(message):
    num_zakaz = message.get_args()
    if len(num_zakaz) == 0:
        await message.answer("Вы не ввели номер заказа `/status X`", parse_mode='markdown')
    elif not num_zakaz.isdigit():
        await message.answer("Введите число")

    else:
        connection, cursor = connect_data_b()
        cursor.execute("SELECT zakaz,data FROM zakaz WHERE zakaz = %s", (num_zakaz,))
        result = cursor.fetchone()

        cursor.close()
        connection.close()
        if result:
            await message.answer(f'Заказ № {result[0]} принят\n\nВремя: {result[1]}')

        else:
            await message.answer(f'Заказ № {num_zakaz} не найден в списке принятых')
        cursor.close()
        connection.close()


async def delete_user_zakaz(message: types.Message):
    await message.delete()
    args = message.text.split('/del_zakaz ', 1)[1].split()

    if len(args) != 2:
        await message.answer("Неверный формат команды.\nИспользуйте /del_zakaz <chat_id> <message_id>",
                             parse_mode='markdown')
        return

    chat_id, message_id = args

    try:
        await bot.delete_message(chat_id, message_id)
        print(f"Сообщение в чате {chat_id}, с идентификатором {message_id} успешно удалено.")
        await message.answer('Заказ удален')
    except Exception as e:
        print(f"Ошибка удаления сообщения: {e}")
        await message.answer("Произошла ошибка при удалении заказа.\nВозможно заказ удален!")
