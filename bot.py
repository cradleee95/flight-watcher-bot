import requests
import time
import logging
from telegram import Bot
from datetime import datetime

# Telegram Bot Token
TELEGRAM_TOKEN = "7796364848:AAEMV8VEYPdX7WDHIWpk5Wc4zTzmMLbY4vc"
CHAT_ID = None  # Будет определён после первого сообщения от пользователя

# Настройки маршрута
FROM = "CEK"  # Челябинск
TO = "AYT"    # Анталья
DEPARTURE_DATE = "2025-04-23"
RETURN_DATE = "2025-05-06"
MAX_PRICE = 24000

# Логгер
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TELEGRAM_TOKEN)

# Заглушка: тут будет реальный API/парсинг
def check_price():
    # Пример найденного билета
    test_price = 23900  # Цена ниже 24000
    direct_flight = True
    baggage_kg = 20
    carry_on_kg = 8

    if test_price < MAX_PRICE and direct_flight and baggage_kg >= 20 and carry_on_kg >= 8:
        return test_price
    return None

# Проверка и отправка уведомления
def run_check():
    global CHAT_ID
    price = check_price()
    if price:
        message = (
            f"🚀 Найден билет!
"
            f"Челябинск → Анталья\n"
            f"Даты: {DEPARTURE_DATE} - {RETURN_DATE}\n"
            f"Цена: {price} ₽\n"
            f"Условия: прямой рейс, багаж 20кг+, ручная кладь 8кг+"
        )
        if CHAT_ID:
            bot.send_message(chat_id=CHAT_ID, text=message)
        else:
            logging.info("CHAT_ID ещё не установлен. Сообщение не отправлено.")

# Telegram polling для получения CHAT_ID
from telegram.ext import Updater, MessageHandler, Filters

def start_handler(update, context):
    global CHAT_ID
    CHAT_ID = update.message.chat_id
    context.bot.send_message(chat_id=CHAT_ID, text="✅ Бот активен! Буду присылать уведомления, как только цена упадёт ниже 24 000₽")

def main():
    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, start_handler))
    updater.start_polling()
    logging.info("Бот запущен")

    # Проверка каждые 20 минут
    while True:
        if CHAT_ID:
            logging.info(f"Проверка билетов: {datetime.now()}")
            run_check()
        time.sleep(1200)  # 20 минут = 1200 секунд

if __name__ == '__main__':
    main()
