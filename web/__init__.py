#@hdfilm0900_bot
from flask import Flask

web_app = Flask(__name__)

@web_app.route('/')
def health_check():
    return "Bot is running with Flask!", 200
