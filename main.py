import os
from flask import Flask
from threading import Thread
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

# Web Server အတွက်
app = Flask(__name__)
@app.route('/')
def home():
    return "Bot is running 24/7!"

def run_web():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

# Commands
async def start(update, context):
    await update.message.reply_text('မင်္ဂလာပါ! ကျွန်တော်က သင်နဲ့အတူ တွဲလုပ်မယ့် အဆင့်မြင့် Bot ပါ။')

async def weather(update, context):
    await update.message.reply_text('ယခုအချိန်တွင် ရန်ကုန်မြို့၌ အပူချိန် ၃၂ ဒီဂရီစင်တီဂရိတ် ရှိပါတယ်။')

async def info(update, context):
    user = update.effective_user
    await update.message.reply_text(f'သင့်နာမည်: {user.first_name}\nသင့် ID: {user.id}')

async def echo(update, context):
    text = update.message.text
    await update.message.reply_text(f'သင်ပြောတာကို ကျွန်တော် စိတ်ဝင်တစား နားထောင်နေပါတယ်: "{text}"')

if __name__ == '__main__':
    # Web server စတင်ခြင်း
    t = Thread(target=run_web)
    t.start()
    
    # သင့် Token
    TOKEN = "8829581045:AAFlpGC-6fPS0UTRZSbAz1ToPz4QusMxiOc"
    
    app_bot = ApplicationBuilder().token(TOKEN).build()
    
    # Handlers
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(CommandHandler("weather", weather))
    app_bot.add_handler(CommandHandler("info", info))
    app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    
    app_bot.run_polling()
 app_bot.run_polling()
    
