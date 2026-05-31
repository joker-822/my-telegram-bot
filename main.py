import os
from flask import Flask
from threading import Thread
from telegram import ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

app = Flask(__name__)
@app.route('/')
def home():
    return "Bot is active!"

def run_web():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

# ခလုတ်များ တည်ဆောက်ခြင်း
def get_main_keyboard():
    keyboard = [['/weather', '/info'], ['/help']]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# Commands
async def start(update, context):
    await update.message.reply_text(
        'မင်္ဂလာပါ! ကျွန်တော်က သင်နဲ့အတူ တွဲလုပ်မယ့် အဆင့်မြင့် Bot ပါ။ အောက်ပါခလုတ်များကို သုံးနိုင်ပါတယ်။',
        reply_markup=get_main_keyboard()
    )

async def weather(update, context):
    await update.message.reply_text('ရန်ကုန်မြို့တွင် အပူချိန် ၃၂ ဒီဂရီစင်တီဂရိတ် ရှိပါတယ်။')

async def info(update, context):
    user = update.effective_user
    await update.message.reply_text(f'သင့်အချက်အလက်:\nနာမည်: {user.first_name}\nID: {user.id}')

async def help_cmd(update, context):
    await update.message.reply_text('ကျွန်တော်က သင့်ကို ရာသီဥတုစစ်ပေးခြင်း၊ သင့်အချက်အလက်ပြခြင်းများ လုပ်ပေးနိုင်ပါတယ်။')

async def echo(update, context):
    text = update.message.text
    await update.message.reply_text(f'သင်ပြောတာကို ကျွန်တော် နားထောင်နေပါတယ်: "{text}"')

if __name__ == '__main__':
    # Web server
    t = Thread(target=run_web)
    t.start()
    
    TOKEN = "8829581045:AAFlpGC-6fPS0UTRZSbAz1ToPz4QusMxiOc"
    
    app_bot = ApplicationBuilder().token(TOKEN).build()
    
    # Handlers
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(CommandHandler("weather", weather))
    app_bot.add_handler(CommandHandler("info", info))
    app_bot.add_handler(CommandHandler("help", help_cmd))
    app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    
    app_bot.run_polling()
    
