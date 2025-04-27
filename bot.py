import telebot
from user import user
from config import  *
# Создайте объект бота с вашим токеном
TOKEN = TOKEN
bot = telebot.TeleBot(TOKEN)

# Списки для хранения данных
users = {}
# Команда /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Я бот. Используй команды:\n"
                                      "/blacklist - ввести черный список тем\n"
                                      "/urls - ввести URL-адреса\n"
                                      "/repeat_urls - повторить все URL-адреса")
    try:
        temp = users[f"{message.chat.id}"]
    except Exception:
        users[f"{message.chat.id}"] = user(message)

# Команда /blacklist - для ввода черного списка тем
@bot.message_handler(commands=['blacklist'])
def handle_blacklist(message):
    bot.send_message(message.chat.id, "Отправь мне темы, которые ты хочешь добавить в черный список. "
                                      "Они будут разделены запятой.")

    # Устанавливаем ожидание следующего ввода
    bot.register_next_step_handler(message, process_blacklist)

# Обработчик для черного списка
def process_blacklist(message):
    active_user = users[f"{message.chat.id}"]
    active_user.set_banlist(message.text)
    bot.send_message(message.chat.id, f"Черный список обновлен: {', '.join(users[f"{message.chat.id}"].get_banlist())}")
    

# Команда /urls - для ввода URL-адресов
@bot.message_handler(commands=['urls'])
def handle_urls(message):
    bot.send_message(message.chat.id, "Отправь мне URL-адреса, хочешь обработать. "
                                      "Они будут разделены запятой или переходом на следующую строку")

    # Устанавливаем ожидание следующего ввода
    bot.register_next_step_handler(message, process_urls)

# Обработчик для URL-адресов
def process_urls(message):
    active_user = users[f"{message.chat.id}"]
    active_user.set_message(message)
    result = active_user.check_urls()
    bot.send_message(message.chat.id, result)



# Команда /repeat_urls - для повторения URL-адресов
@bot.message_handler(commands=['repeat_urls'])
def repeat_urls(message):
    active_user = users[f"{message.chat.id}"]
    result = active_user.check_urls()
    bot.send_message(message.chat.id, result)

# Запуск бота
bot.polling()
