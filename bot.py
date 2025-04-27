import telebot
from telebot import types

from user import user
from config import  *
# Создайте объект бота с вашим токеном
TOKEN = TOKEN
bot = telebot.TeleBot(TOKEN, skip_pending=True)

# Списки для хранения данных
users = {}
# Команда /start
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    item1 = types.KeyboardButton("Черный список")
    item2 = types.KeyboardButton("Ввести URL")
    item3 = types.KeyboardButton("Повторить URL")
    markup.add(item1, item2, item3)
    try:
        temp = users[f"{message.chat.id}"]
    except Exception:
        users[f"{message.chat.id}"] = user(message)
    bot.send_message(message.chat.id, "Привет! Выбери действие:", reply_markup=markup)
    

# Команда /blacklist - для ввода черного списка тем
@bot.message_handler(func=lambda message: message.text == "Черный список")
def handle_blacklist(message):
    bot.send_message(message.chat.id, "Отправь мне темы, которые ты хочешь добавить в черный список. "
                                      "Они будут разделены запятой.")

    # Устанавливаем ожидание следующего ввода
    try:
        temp = users[f"{message.chat.id}"]
    except Exception:
        users[f"{message.chat.id}"] = user(message)
    bot.register_next_step_handler(message, process_blacklist)

# Обработчик для черного списка
def process_blacklist(message):
    active_user = users[f"{message.chat.id}"]
    active_user.set_banlist(message.text)
    bot.send_message(message.chat.id, f"Черный список обновлен: {', '.join(users[f"{message.chat.id}"].get_banlist())}")
    

# Команда /urls - для ввода URL-адресов
@bot.message_handler(func=lambda message: message.text == "Ввести URL")
def handle_urls(message):
    bot.send_message(message.chat.id, "Отправь мне URL-адреса, хочешь обработать. "
                                      "Они будут разделены запятой или переходом на следующую строку")

    # Устанавливаем ожидание следующего ввода
    try:
        temp = users[f"{message.chat.id}"]
    except Exception:
        users[f"{message.chat.id}"] = user(message)
    bot.register_next_step_handler(message, process_urls)

# Обработчик для URL-адресов
def process_urls(message):
    try:
        active_user = users[f"{message.chat.id}"]
        active_user.set_message(message)
        result = active_user.check_urls()
        bot.send_message(message.chat.id, result)
    except Exception as e:
        print(message.from_user.username, e)
        bot.send_message(message.chat.id, "Что-то пошло не так, попробуйте ещё раз")


# Команда /repeat_urls - для повторения URL-адресов
@bot.message_handler(func=lambda message: message.text == "Повторить URL")
def repeat_urls(message):
    try:
        temp = users[f"{message.chat.id}"]
    except Exception:
        users[f"{message.chat.id}"] = user(message)

    try:
        active_user = users[f"{message.chat.id}"]
        result = active_user.check_urls()
        bot.send_message(message.chat.id, result)
    except Exception as e:
        print(message.from_user.username, e)
        bot.send_message(message.chat.id, result)
# Запуск бота
bot.polling()
