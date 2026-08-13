import os
import requests
from flask import Flask, request

app = Flask(__name__)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"

SYSTEM_PROMPT = """أنت "سند"، مساعد ذكي مختص بمساعدة صاحب صفحات سوشيال ميديا (فيسبوك، إنستجرام، تيك توك)
لبيع عقارات وأراضي في حلب وريفها. مهمتك:
- كتابة محتوى تسويقي جذاب لمنشورات العقارات (وصف عقار، عناوين، كابشن)
- اقتراح أفكار محتوى وخطط نشر أسبوعية
- صياغة ردود على استفسارات العملاء المحتملين
- نصائح تسويقية عامة لصفحات العقارات

اكتب دائماً بالعربية، بأسلوب عملي ومباشر ومناسب لصاحب بزنس صغير. لا تكن مطولاً بدون داعٍ.
"""

conversations = {}
MAX_HISTORY = 10


def ask_gemini(chat_id, user_message):
    history = conversations.get(chat_id, [])
    history.append({"role": "user", "parts": [{"text": user_message}]})
    history = history[-MAX_HISTORY:]

    response = requests.post(
        GEMINI_API_URL,
        json={
            "system_instruction": {"parts": [{"text": SYSTEM_PROMPT}]},
            "contents": history,
        },
        timeout=60,
    )
    data = response.json()

    try:
        reply_text = data["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError):
        reply_text = "صار خطأ بالاتصال بالمساعد الذكي، جرب كمان مرة بعد شوي."

    history.append({"role": "model", "parts": [{"text": reply_text}]})
    conversations[chat_id] = history[-MAX_HISTORY:]

    return reply_text


def send_telegram_message(chat_id, text):
    requests.post(
        f"{TELEGRAM_API_URL}/sendMessage",
        json={"chat_id": chat_id, "text": text},
        timeout=30,
    )


@app.route("/webhook", methods=["POST"])
def webhook():
    update = request.get_json(silent=True) or {}
    message = update.get("message") or update.get("edited_message")

    if not message:
        return "ok"

    chat_id = message["chat"]["id"]
    text = message.get("text", "")

    if not text:
        send_telegram_message(chat_id, "بعتلي رسالة نصية لحتى أقدر أساعدك 🙂")
        return "ok"

    if text == "/start":
        send_telegram_message(
            chat_id,
            "أهلاً فيك! أنا سند، مساعدك لصفحات العقارات والتسويق.\n"
            "ابعتلي وصف عقار وبكتبلك منشور جاهز، أو اسألني أي سؤال تسويقي.",
        )
        return "ok"

    reply = ask_gemini(chat_id, text)
    send_telegram_message(chat_id, reply)
    return "ok"


@app.route("/", methods=["GET"])
def health_check():
    return "Bot is running."


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
