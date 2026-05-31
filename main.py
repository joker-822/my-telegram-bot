import os
from flask import Flask
from threading import Thread
from datetime import datetime
from telegram import ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

app = Flask(__name__)
@app.route('/')
def home():
    return "Bot is running perfectly!"

def run_web():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

# ခလုတ်များ
def get_keyboard():
    return ReplyKeyboardMarkup([['/weather', '/time'], ['/info', '/help']], resize_keyboard=True)

# Commands
async def start(update, context):
    await update.message.reply_text("မင်္ဂလာပါ! ကျွန်တော်က သင့်ရဲ့ အစွမ်းထက် Helper Bot ပါ။ ဘာများ ကူညီပေးရမလဲ?", reply_markup=get_keyboard())

async def weather(update, context):
    await update.message.reply_text('🌡 ရန်ကုန်မြို့တွင် လက်ရှိ ၃၂ ဒီဂရီစင်တီဂရိတ် ရှိပါသည်။')

async def get_time(update, context):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    await update.message.reply_text(f'⏰ လက်ရှိအချိန်: {now}')

async def info(update, context):
    user = update.effective_user
    await update.message.reply_text(f'👤 အသုံးပြုသူအချက်အလက်:\nနာမည်: {user.first_name}\nID: {user.id}\nUsername: @{user.username}')

async def echo(update, context):
    # AI မပါပေမယ့် စာပြန်တဲ့စနစ်
    text = update.message.text
    await update.message.reply_text(f'သင်ပြောတာကို ကျွန်တော် မှတ်သားထားပါတယ်: "{text}"')

if __name__ == '__main__':
    t = Thread(target=run_web)
    t.start()
    
    TOKEN = "8829581045:AAFlpGC-6fPS0UTRZSbAz1ToPz4QusMxiOc"
    
    app_bot = ApplicationBuilder().token(TOKEN).build()
    
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(CommandHandler("weather", weather))
    app_bot.add_handler(CommandHandler("time", get_time))
    app_bot.add_handler(CommandHandler("info", info))
    app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    
    app_bot.run_polling()
    
