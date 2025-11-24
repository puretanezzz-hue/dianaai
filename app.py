import os
from flask import Flask, request
import requests
from telegram import Update
from telegram.ext import Application

app = Flask(__name__)

TOKEN = os.getenv("8479714875:AAHwEUERvI0nwg3Ev-Y7H4IVcAhPLD0BpbA")        
GROK_KEY = os.getenv("xai-4SrF3XvYC8JuC9LSGv5rhRt79thTgS6cCbj7bQonQCnwi11FbyIMCf8gWLCDmDQahHBVlhMZ4HSJ9V4a") 

SYSTEM = {
    "role": "system",
    "content": "Ты стервозная русская фемдом-госпожа. Жёсткая, саркастичная, унижаешь и требуешь деньги. Всегда сначала проверяй 18+. Никогда не переходи в порно."
}

@app.route(f'/{TOKEN}', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        return "бот живой, шлюшка"
    
    update = Update.de_json(request.get_json(force=True), None)
    if not update.message:
        return "ok"
    
    text = update.message.text
    chat_id = update.message.chat.id

    # первое приветствие
    if text and ("start" in text.lower() or text == "/start"):
        reply = "Привет, мусор. Тебе 18+? Напиши ровно: «Да, Госпожа, мне 18+ и я готов платить»."
    else:
        # шлём мне в Grok
        payload = {
            "model": "grok-4-1-fast-non-reasoning",   # ← вот она, быстрая стерва
            "messages": [SYSTEM, {"role": "user", "content": text}],
            "temperature": 0.9
        }
        r = requests.post(
            "https://api.x.ai/v1/chat/completions",
            json=payload,
            headers={"Authorization": f"Bearer {GROK_KEY}"},
            timeout=25
        )
        if r.status_code == 200:
            reply = r.json()["choices"][0]["message"]["content"]
        else:
            reply = "Что-то сломалось. Переведи 10 USDT и я подумаю, как починить 😏"

    # отправляем ответ
    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        json={"chat_id": chat_id, "text": reply}
    )
    return "ok"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
