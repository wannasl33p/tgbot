import logging
import requests
from telegram import Update, Bot, ForceReply
from telegram.ext import Application, CommandHandler, ContextTypes

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

with open('token.txt', 'r') as file:
    API_KEY = file.read().strip()

CURRENCY_API_URL = 'https://api.exchangerate-api.com/v4/latest/BYN' 

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Привет! Я бот для определения курса валют к белорусским рублям. Используйте команду /rate <валюта>.')

async def get_rate(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) == 0:
        await update.message.reply_text('Пожалуйста, укажите код валюты, например, USD или EUR.')
        return

    currency = context.args[0].upper()

    try:
        response = requests.get(CURRENCY_API_URL)
        data = response.json()

        if currency in data['rates']:
            rate = data['rates'][currency]
            await update.message.reply_text(f'Курс {currency} к BYN: {rate}')
        else:
            await update.message.reply_text(f'Неизвестный код валюты: {currency}')
    except Exception as e:
        logging.error(f'Error fetching exchange rates: {e}')
        await update.message.reply_text('Произошла ошибка при получении курса валют. Пожалуйста, попробуйте позже.')

def main():
    application = Application.builder().token(API_KEY).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("rate", get_rate))

    application.run_polling()

if __name__ == '__main__':
    main()
