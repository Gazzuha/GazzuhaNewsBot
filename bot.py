# 📦 Telegram бот "Game Events Tracker"
# Работает на Render.com, читает Reddit и шлёт игровые новости

import os
import logging
import threading
import time
from flask import Flask
import telegram
from telegram.ext import Updater, CommandHandler
import praw

# ----- Логгирование -----
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# ----- Переменные окружения -----
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_SECRET = os.getenv("REDDIT_SECRET")
REDDIT_USER_AGENT = "GameEventsBot/0.1"

# ----- Reddit API -----
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_SECRET,
    user_agent=REDDIT_USER_AGENT
)

# ----- Telegram Команды -----
def start(update, context):
    update.message.reply_text(
        "👾 Привет! Я бот, который следит за игровыми событиями: ARG, челленджи, Steam фесты и т.д.\n"
        "Напиши /events чтобы получить свежие новости."
    )

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

# ----- Запуск бота -----
def run_bot():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("events", events))

    logging.info("🚀 Telegram-бот запущен")
    updater.start_polling()
    updater.idle()

# ----- Flask-заглушка для Render -----
app = Flask(__name__)

@app.route('/')
def index():
    return "Bot is running!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))  # Берём порт из окружения или ставим 10000
    logging.info(f"🌐 Flask-заглушка на порту {port}")
    app.run(host="0.0.0.0", port=port)

# ----- Запуск в потоках -----
if __name__ == '__main__':
    threading.Thread(target=run_bot).start()
    threading.Thread(target=run_flask).start()

    while True:
        time.sleep(10)  # Чтобы главный поток не завершался
