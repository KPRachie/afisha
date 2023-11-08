from sqlite3 import connect
import telebot

token = "6379993313:AAHTPaOdSg1tLxQod_c0XfjOoGug-5TMbPI"
bot = telebot.TeleBot(token=token)
users = {}
answers = {}
crets = {}


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Привет! Введи своё имя:")
    user_id = message.chat.id
    if user_id not in users:
        users[user_id] = message.text


@bot.message_handler(commands=["afisha"])
def afisha(message):
    sent_message = bot.send_message(message.chat.id, "Напишите, запрос поиска:")
    bot.register_next_step_handler(sent_message, search)


def search(message):
    bot.send_message(message.chat.id, message.text)
    conn = connect("coservatort.sqlite")
    query = message.text
    cursor = conn.execute(
        "SELECT hall, title, song, link, date FROM con1 WHERE hall like ? or title like ? or song like ? or link like ? or date like ?",
        ["%{}%".format(query), "%{}%".format(query), "%{}%".format(query),
         "%{}%".format(query), "%{}%".format(query)])
    con = cursor.fetchall()
    counter = 0
    for i in con:
        if counter < 5:
            bot.send_message(message.chat.id, "\n\n".join(i))
        counter += 1
    conn.commit()
    conn.close()


@bot.message_handler(content_types=['text'])
def answer(message):
    bot.send_message(message.chat.id,
                     "Для того, чтобы подобрать концерт, введите /afisha.")


bot.polling(none_stop=True)
