# دليل تشغيل بوت "سند" — مجاني بالكامل

## 1) البوت على تيليجرام
- افتح تيليجرام، دور على BotFather، اكتب /newbot، اختار اسم ويوزرنيم
- احفظ الـ Token

## 2) مفتاح Gemini (مجاني)
- افتح aistudio.google.com/apikey وخد مفتاح API

## 3) الكود على GitHub
- تم رفعه هلق

## 4) الاستضافة المجانية (Render)
- سجل بـ render.com
- New + ثم Web Service ثم اختار الريبو
- Build Command: pip install -r requirements.txt
- Start Command: gunicorn app:app
- Instance Type: Free
- Environment Variables: TELEGRAM_TOKEN و GEMINI_API_KEY

## 5) الربط النهائي
افتح: https://api.telegram.org/bot<TOKEN>/setWebhook?url=https://YOUR-APP.onrender.com/webhook

## ملاحظة
Render المجاني بينام لو ما حدا استخدمه، وبياخد كم ثانية يصحى.
