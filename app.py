from flask import Flask, request
import requests
import os

app = Flask(__name__)

TOKEN = os.getenv("BOT_TOKEN")
BASE_URL = f"https://tapi.bale.ai/bot{TOKEN}"

def send_message(chat_id, text):
    url = f"{BASE_URL}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": text
    }
    requests.post(url, json=data)

@app.route("/", methods=["GET"])
def home():
    return "Bot is running"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    if data:
        message = data.get("message", {})
        chat_id = message.get("chat", {}).get("id")
        text = message.get("text", "")

        if text == "/start":
            send_message(
                chat_id,
                "سلام 🌹\nبه ربات موسسه زیست و شیمی کنکور خوش آمدید."
            )

    return "ok"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)