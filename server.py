from flask import Flask
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "Бот работает!"

def run():
    port = int(os.environ.get("PORT", 80))
    app.run(host="0.0.0.0", port=port)

def keep_alive():
    from threading import Thread
    t = Thread(target=run)
    t.start()
