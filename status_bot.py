from config import TOKEN
from aiogram import Bot
from datetime import datetime
import pytz  # pip install pytz

bot = Bot(token=TOKEN)


async def on_startup(dispatcher):  # Отправка сообщения при запуске бота
    moscow_time = datetime.now(pytz.timezone('Europe/Moscow')).strftime("%Y-%m-%d %H:%M:%S")
    await bot.send_message(chat_id=5869013585, text=f"Бот запущен! {moscow_time}MSK")
