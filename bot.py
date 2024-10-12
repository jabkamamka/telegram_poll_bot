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
    bot.reply_to(message, "Привет! Оцените мероприятие: напишите 'хорошо', 'нормально' или 'плохо'.")

# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def handle_vote(message):
    text = message.text.lower()
    if text in ['хорошо', 'нормально', 'плохо']:
        votes[text] += 1
        bot.reply_to(message, f"Спасибо за ваш голос! Вы выбрали '{text}'.")
    else:
        bot.reply_to(message, "Пожалуйста, выберите 'хорошо', 'нормально' или 'плохо'.")

# Создание веб-приложения Flask
app = Flask(__name__)

@app.route('/')
def index():
    total_votes = sum(votes.values())
    percentages = {}
    if total_votes > 0:
        percentages['хорошо'] = round((votes['хорошо'] / total_votes) * 100)
        percentages['нормально'] = round((votes['нормально'] / total_votes) * 100)
        percentages['плохо'] = round((votes['плохо'] / total_votes) * 100)
    else:
        percentages['хорошо'] = 0
        percentages['нормально'] = 0
        percentages['плохо'] = 0

    return render_template('index.html', percentages=percentages)

# Запуск веб-приложения в отдельном потоке
def run_app():
    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    # Запуск Flask в отдельном потоке
    threading.Thread(target=run_app).start()
    # Запуск бота
    bot.polling(none_stop=True)
