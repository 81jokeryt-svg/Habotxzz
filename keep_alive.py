import os
from flask import Flask
from threading import Thread

app = Flask(__name__)

@app.route('/')
def index():
    return "Bot is Alive!"

def run():
    # Render ke liye PORT 10000 zaroori hai
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

def start_server():
    t = Thread(target=run)
    t.start()

