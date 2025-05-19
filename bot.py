# 📦 Telegram бот "Game Events Tracker"
# Работает на Render.com, читает Reddit и шлёт игровые новости

import os
import logging
import telegram
from telegram.ext import Updater, CommandHandler
import praw
from datetime import datetime

# Настройка логгирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Получаем токены и параметры из переменных окружения
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_SECRET = os.getenv("REDDIT_SECRET")
REDDIT_USER_AGENT = "GameEventsBot/0.1"

# Инициализация Reddit API
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_SECRET,
    user_agent=REDDIT_USER_AGENT
)

# Команда /start
def start(update, context):
    update.message.reply_text(
        "👾 Привет! Я бот, который следит за игровыми событиями: ARG, челленджи, Steam фесты и т.д.\n"
        "Напиши /events чтобы получить свежие новости."
    )

# Команда /events — показать свежие посты

def events(update, context):
    subreddits = ["GameDetectives", "Games"]
    limit = 5
    messages = []
    for sub in subreddits:
        subreddit = reddit.subreddit(sub)
        messages.append(f"🔥 Топ из r/{sub}:")
        for post in subreddit.hot(limit=limit):
            if not post.stickied:
                messages.append(f"• [{post.title}]({post.url})")
    full_message = "\n".join(messages)
    update.message.reply_text(full_message, parse_mode=telegram.constants.ParseMode.MARKDOWN)

# Главная функция запуска

def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("events", events))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
    
    # Заглушка для Render — не даёт ошибку из-за порта
from flask import Flask
import threading

app = Flask(__name__)

@app.route('/')
def index():
    return "Bot is running"

def run_flask():
    app.run(host="0.0.0.0", port=10000)

# Запускаем Flask в отдельном потоке
threading.Thread(target=run_flask).start()
