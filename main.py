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
    await update.message.reply_text('ယခုအချိန်တွင် ရန်ကုန်မြို့၌ အပူချိန် ၃၂ ဒီဂရီစင်တီဂရိတ် ရှိပါတယ်။')

async def echo(update, context):
    text = update.message.text
    await update.message.reply_text(f'သင်ပြောတာကို ကျွန်တော် စိတ်ဝင်တစား နားထောင်နေပါတယ်: "{text}"')

if __name__ == '__main__':
    t = Thread(target=run_web)
    t.start()
    
    # သင့် Token ကို တစ်ခါတည်း ထည့်ပေးလိုက်ပါပြီ
    TOKEN = "8829581045:AAFlpGC-6fPS0UTRZSbAz1ToPz4QusMxiOc"
    
    app_bot = ApplicationBuilder().token(TOKEN).build()
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(CommandHandler("weather", weather))
    app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    
    app_bot.run_polling()
    
