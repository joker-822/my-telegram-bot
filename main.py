import os
import requests
from flask import Flask
from threading import Thread
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

app = Flask(__name__)
@app.route('/')
def home():
    return "Bot is active!"

def run_web():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

# Commands
async def start(update, context):
    await update.message.reply_text('မင်္ဂလာပါ! ကျွန်တော်က သင်နဲ့အတူ တွဲလုပ်မယ့် အဆင့်မြင့် Bot ပါ။')

async def weather(update, context):
    # ရိုးရှင်းတဲ့ ရာသီဥတုစစ်ဆေးခြင်း (ဥပမာ)
    await update.message.reply_text('ယခုအချိန်တွင် ရန်ကုန်မြို့၌ အပူချိန် ၃၂ ဒီဂရီစင်တီဂရိတ် ရှိပါတယ်။')

async def echo(update, context):
    # စာကို ပြန်ပြင်ပြီး ပိုမိုဖော်ရွေစွာ ပြောဆိုခြင်း
    text = update.message.text
    await update.message.reply_text(f'သင်ပြောတာကို ကျွန်တော် စိတ်ဝင်တစား နားထောင်နေပါတယ်: "{text}"')

if __name__ == '__main__':
    t = Thread(target=run_web)
    t.start()
    
    # Token ကို Render Environment Variable ကနေ ခေါ်သုံးပါ
    TOKEN = os.environ.get("BOT_TOKEN")
    
    app_bot = ApplicationBuilder().token(TOKEN).build()
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(CommandHandler("weather", weather))
    app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    
    app_bot.run_polling()
    
