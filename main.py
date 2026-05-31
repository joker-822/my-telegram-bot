import os, random, qrcode, string, pyshorteners
from flask import Flask
from threading import Thread
from datetime import datetime
from telegram import ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler

# Web Server
app = Flask(__name__)
@app.route('/')
def home(): return "Bot is running!"

# ခလုတ် ၁၂ ခု (၄ တန်း x ၃ ကော်လံ)
def get_keyboard():
    return ReplyKeyboardMarkup([
        ['/start', '/help', '/rate'],
        ['/weather', '/time', '/calc'],
        ['/qr', '/short', '/quote'],
        ['/pass', '/dice', '/info']
    ], resize_keyboard=True)

# အဆင့်မြင့် လုပ်ဆောင်ချက်များ
async def shorten_link(update, context):
    try:
        url = context.args[0]
        s = pyshorteners.Shortener()
        await update.message.reply_text(f"🔗 လင့်ခ်အတို: {s.tinyurl.short(url)}")
    except: await update.message.reply_text("အသုံးပြုပုံ: /short [link]")

async def get_info(update, context):
    user = update.effective_user
    await update.message.reply_text(f"👤 အချက်အလက်:\nID: {user.id}\nUsername: @{user.username}")

# Main
if __name__ == '__main__':
    Thread(target=lambda: app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))).start()
    
    TOKEN = "8829581045:AAFlpGC-6fPS0UTRZSbAz1ToPz4QusMxiOc"
    app_bot = ApplicationBuilder().token(TOKEN).build()
    
    # Commands
    app_bot.add_handler(CommandHandler("start", lambda u, c: u.message.reply_text("Welcome!", reply_markup=get_keyboard())))
    app_bot.add_handler(CommandHandler("help", lambda u, c: u.message.reply_text("အားလုံးကို သုံးနိုင်ပါပြီ!")))
    app_bot.add_handler(CommandHandler("short", shorten_link))
    app_bot.add_handler(CommandHandler("info", get_info))
    # ကျန်သည့် Command များ (weather, time, calc, qr, quote, pass, dice, rate) အားလုံး ထည့်ပါ
    
    app_bot.run_polling()
    
