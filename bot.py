import telebot
from flask import Flask, render_template
from collections import defaultdict
import threading

API_TOKEN = '7781217820:AAFlE7zJjNIhccJN4HcB6sprR2daPZuxVOM'  # Замените на токен вашего бота

bot = telebot.TeleBot(API_TOKEN)

# Словарь для хранения голосов
votes = defaultdict(int)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Создание клавиатуры с вариантами голосования
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ['Хорошо', 'Нормально', 'Плохо']
    keyboard.add(*buttons)
    
    bot.send_message(message.chat.id, "Привет! Оцените мероприятие:", reply_markup=keyboard)

# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def handle_vote(message):
    text = message.text.lower()
    if text in ['хорошо', 'нормально', 'плохо']:
        votes[text] += 1
        bot.reply_to(message, f"Спасибо за ваш голос! Вы выбрали '{text}'.")
    else:
        bot.reply_to(message, "Пожалуйста, выберите 'Хорошо', 'Нормально' или 'Плохо' с помощью кнопок.")

# Создание веб-приложения Flask
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', votes=votes)

# Запуск веб-приложения в отдельном потоке
def run_app():
    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    # Запуск Flask в отдельном потоке
    threading.Thread(target=run_app).start()
    # Запуск бота
    bot.polling(none_stop=True)
