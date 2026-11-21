import os
import telebot
from gigachat import GigaChat

TELEGRAM_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
GIGA_KEY = os.environ["GIGACHAT_KEY"]

bot = telebot.TeleBot(TELEGRAM_TOKEN)
giga = GigaChat(credentials=GIGA_KEY, scope="GIGACHAT_API_PERS", verify_ssl_certs=False)

@bot.message_handler(commands=["start"])
def start(m):
    bot.reply_to(m, "Привет! Я Решалка. Напиши задачу — помогу решить.")

@bot.message_handler(content_types=["text"])
def solve(m):
    try:
        resp = giga.chat("Ты дружелюбный помощник. Реши задачу коротко и понятно. Задача: " + m.text)
        bot.reply_to(m, resp.choices[0].message.content)
    except Exception as e:
        print("Ошибка GigaChat:", e)
        bot.reply_to(m, "Не получилось спросить GigaChat: " + str(e))

print("Бот запущен!")
bot.infinity_polling()
