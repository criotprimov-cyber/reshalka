import telebot

TELEGRAM_TOKEN = "8943068070:AAGB146oqrdTyocu4HPDOdEShxJ6aoFVO8c"

bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(commands=["start"])
def start(m):
    bot.reply_to(m, "Привет! Бот запущен и работает")

@bot.message_handler(content_types=["text"])
def echo(m):
    bot.reply_to(m, "Понял тебя: " + m.text)

print("Бот запущен!")
bot.infinity_polling()
