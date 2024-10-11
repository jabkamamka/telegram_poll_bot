from flask import Flask, render_template
from bot import votes  # Импортируем словарь голосов из bot.py

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', votes=votes)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
