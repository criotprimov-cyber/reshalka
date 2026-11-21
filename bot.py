import socket
import os
import telebot

TELEGRAM_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
GIGA_KEY = os.environ["GIGACHAT_KEY"]

# Диагностика сети к GigaChat
print("Проверка DNS и соединения с GigaChat...")
try:
    infos = socket.getaddrinfo("ngw.devices.sberbank.ru", 9443)
    ip = infos[0][4][0]
    print("DNS ок: ngw.devices.sberbank.ru =", ip)
except Exception as e:
    print("Ошибка DNS:", e)
    ip = None
if ip:
    try:
        s = socket.create_connection((ip, 9443), timeout=10)
        s.close()
        print("Соединение с портом 9443: ОК")
    except Exception as e:
        print("Соединение с портом 9443: СБОЙ —", e)

bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(commands=["start"])
def start(m):
    bot.reply_to(m, "Привет! Я Решалка. Напиши задачу — помогу решить.")

@bot.message_handler(content_types=["text"])
def solve(m):
    try:
        from gigachat import GigaChat
        giga = GigaChat(credentials=GIGA_KEY, scope="GIGACHAT_API_PERS", verify_ssl_certs=False)
        resp = giga.chat("Ты дружелюбный помощник. Реши задачу коротко и понятно. Задача: " + m.text)
        bot.reply_to(m, resp.choices[0].message.content)
    except Exception as e:
        print("Ошибка GigaChat:", e)
        bot.reply_to(m, "Не получилось спросить GigaChat: " + str(e))

print("Бот запущен!")
bot.infinity_polling()
