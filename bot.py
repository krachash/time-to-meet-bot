

#  python3 bot.py

#  python3 bot.py
from server import keep_alive
import os
import logging
import random
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)

# Задаём конечную дату
TARGET_DATE = datetime(2025, 3, 2, 11, 55, 0)


def get_hours_word(n: int) -> str:
    # Если число заканчивается на 1, но не 11 – "час"
    if n % 10 == 1 and n % 100 != 11:
        return "час"
    # Если число заканчивается на 2, 3, 4, но не 12-14 – "часа"
    elif n % 10 in (2, 3, 4) and n % 100 not in (12, 13, 14):
        return "часа"
    else:
        return "часов"


def get_minutes_word(n: int) -> str:
    # Если число заканчивается на 1, но не 11 – "минута"
    if n % 10 == 1 and n % 100 != 11:
        return "минута"
    # Если число заканчивается на 2, 3, 4, но не 12-14 – "минуты"
    elif n % 10 in (2, 3, 4) and n % 100 not in (12, 13, 14):
        return "минуты"
    else:
        return "минут"

def get_time_remaining() -> str:
    now = datetime.now()
    if now >= TARGET_DATE:
        return "Событие уже наступило!"
    delta = TARGET_DATE - now
    # Вычисляем общее число минут
    total_minutes = int(delta.total_seconds() // 60)
    hours = total_minutes // 60
    minutes = total_minutes % 60
    adjectives = [
        "солнышко", "зайка", "лапочка", "любимая", "милая", "обворожительная",
        "неотразимая", "очаровательная", "радость", "сияющая", "умничка",
        "прелестная", "благородная", "великолепная", "незабываемая",
        "чудесная", "сказочная", "волшебная", "добрая", "изумительная",
        "нежная", "миловидная", "душевная", "яркая", "искренняя", "радостная",
        "золотце", "умопомрачительная", "прекрасная", "неповторимая",
        "бесподобная", "миленькая", "нежнейшая", "тёплая", "сердечная",
        "любящая", "благословенная", "сладкая", "дивная", "изумрудная",
        "нежненькая", "светлая", "миловиднейшая", "неповторимейшая",
        "возвышенная", "грациозная", "утонченная", "обворожительнейшая",
        "золотая"
    ]
    adjective = random.choice(adjectives)
    return (
        f"Осталось {hours} {get_hours_word(hours)} и {minutes} {get_minutes_word(minutes)}.\n"
        f"Дарина {adjective} ❤️")


async def time_command(update: Update,
                       context: ContextTypes.DEFAULT_TYPE) -> None:
    remaining = get_time_remaining()
    await update.message.reply_text(remaining)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    message = (
        "Бот запущен!\n\n"
        "Каждый час я буду отправлять сообщение с оставшимся временем до события.\n"
        "А если вы напишете команду /time, я отправлю время прямо сейчас.")
    await update.message.reply_text(message)

    context.application.job_queue.run_repeating(
        lambda ctx: context.bot.send_message(
            chat_id=ctx.job.data["chat_id"],
            text=f"[Ежечасное сообщение]\n{get_time_remaining()}"),
        interval=3600,
        first=0,
        data={"chat_id": chat_id})


def main():
    TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not TOKEN:
        raise Exception(
            "TELEGRAM_BOT_TOKEN is not set in environment variables.")
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("time", time_command))
    # Run polling in a non-blocking way
    app.run_polling(close_loop=False)


import threading

if __name__ == '__main__':
    # Запускаем веб-сервер в отдельном потоке
    threading.Thread(target=keep_alive).start()
    # Запускаем основную логику бота
    main()
