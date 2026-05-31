import os, random, qrcode, string, pyshorteners
from flask import Flask
from threading import Thread
from datetime import datetime
from telegram import ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler

# Web Server (Render အတွက် လိုအပ်သည်)
app = Flask(__name__)
@app.route('/')
def home(): return "Bot is running 24/7!"

def run_web():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

# မြန်မာလို ပြောင်းထားသော ခလုတ်များ
def get_keyboard():
    return ReplyKeyboardMarkup([
        ['/start', '/help', '/rate'],
        ['/weather', '/time', '/calc'],
        ['/qr', '/short', '/quote'],
        ['/pass', '/dice', '/info']
    ], resize_keyboard=True)

# လုပ်ဆောင်ချက်များ
async def start(update, context): await update.message.reply_text("မင်္ဂလာပါ! ဘာများ ကူညီပေးရမလဲ။", reply_markup=get_keyboard())
async def help_cmd(update, context): await update.message.reply_text("အသုံးပြုနိုင်သော Command များ:\n/rate - ငွေလဲနှုန်း\n/short [link] - လင့်ခ်အတို\n/qr [text] - QR ပြုလုပ်ရန်\n/pass [length] - Password ထုတ်ရန်")
async def get_time(update, context): await update.message.reply_text(f"လက်ရှိအချိန်: {datetime.now().strftime('%H:%M:%S')}")
async def roll_dice(update, context): await update.message.reply_dice()
async def get_info(update, context): await update.message.reply_text(f"User ID: {update.effective_user.id}\nUsername: @{update.effective_user.username}")
async def shorten_link(update, context): 
    try: await update.message.reply_text(f"🔗 လင့်ခ်အတို: {pyshorteners.Shortener().tinyurl.short(context.args[0])}")
    except: await update.message.reply_text("အသုံးပြုပုံ: /short [link] ကို ရိုက်ပေးပါ။")

if __name__ == '__main__':
    Thread(target=run_web).start()
    TOKEN = "8829581045:AAFlpGC-6fPS0UTRZSbAz1ToPz4QusMxiOc"
    app_bot = ApplicationBuilder().token(TOKEN).build()
    
    # Command Handler များ
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(CommandHandler("help", help_cmd))
    app_bot.add_handler(CommandHandler("time", get_time))
    app_bot.add_handler(CommandHandler("dice", roll_dice))
    app_bot.add_handler(CommandHandler("info", get_info))
    app_bot.add_handler(CommandHandler("short", shorten_link))
    
    app_bot.run_polling()
    
