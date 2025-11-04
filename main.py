from bot import bot
from config import DISCORD_API_KEY

from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Professor Oak is online!"

def run():
    app.run(host='0.0.0.0', port=8080)

Thread(target=run).start()


if __name__ == "__main__":
    bot.run(DISCORD_API_KEY)
