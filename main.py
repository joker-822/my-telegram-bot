import os
from flask import Flask
from threading import Thread
from openai import OpenAI
from telegram import ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

# Configuration
TOKEN = "8829581045:AAFlpGC-6fPS0UTRZSbAz1ToPz4QusMxiOc"
client = OpenAI(api_key="YOUR_OPENAI_API_KEY") # ဤနေရာတွင် သင့် API Key ထည့်ပါ

app = Flask(__name__)
@app.route('/')
def home():
    return "Bot is running 24/7!"

def run_web():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

# Keyboard Layout
def get_keyboard():
    return ReplyKeyboardMarkup([['/weather', '/info'], ['/help']], resize_keyboard=True)

# Commands
async def start(update, context):
    await update.message.reply_text("မင်္ဂလာပါ! ကျွန်တော်က သင်၏ စမတ်ကျသော AI Assistant ပါ။", reply_markup=get_keyboard())

async def weather(update, context):
    await update.message.reply_text('ယခုအချိန် ရန်ကုန်မြို့တွင် အပူချိန် ၃၂ ဒီဂရီစင်တီဂရိတ် ရှိပါသည်။')

async def info(update, context):
    user = update.effective_user
    await update.message.reply_text(f'👤 အချက်အလက်\nနာမည်: {user.first_name}\nID: {user.id}')

# AI Chat Function
async def chat_with_ai(update, context):
    try:
        user_text = update.message.text
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_text}]
        )
        await update.message.reply_text(response.choices[0].message.content)
    except Exception as e:
        await update.message.reply_text("ဆောရီး! AI စနစ် အလုပ်မလုပ်သေးပါ (API Key စစ်ဆေးပါ)။")

if __name__ == '__main__':
    t = Thread(target=run_web)
    t.start()
    
    app_bot = ApplicationBuilder().token(TOKEN).build()
    
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(CommandHandler("weather", weather))
    app_bot.add_handler(CommandHandler("info", info))
    app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat_with_ai))
    
    app_bot.run_polling()
    
