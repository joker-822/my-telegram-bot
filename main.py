import os, random, qrcode, string, pyshorteners
from flask import Flask
from threading import Thread
from datetime import datetime
from telegram import ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler

app = Flask(__name__)
@app.route('/')
def home(): return "Bot is running 24/7!"
def run_web(): app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

# ဈေးနှုန်းများ
GOLD = "5,800,000"
USD = "4,850"

# ခလုတ်များ (၁၂ ခု)
def get_keyboard():
    return ReplyKeyboardMarkup([
        ['/start', '/help'],
        ['/weather', '/time'],
        ['/calc', '/qr'],
        ['/rate_gold', '/rate_usd'],
        ['/short', '/quote'],
        ['/pass', '/dice', '/info']
    ], resize_keyboard=True)

# Function များ
async def start(update, context): await update.message.reply_text("မင်္ဂလာပါ! အောက်ပါခလုတ်များကို သုံးနိုင်ပါပြီ။", reply_markup=get_keyboard())
async def get_time(update, context): await update.message.reply_text(f"⏰ အချိန်: {datetime.now().strftime('%H:%M:%S')}")
async def rate_gold(update, context): await update.message.reply_text(f"🌟 ရွှေဈေး (1 ကျပ်သား) = {GOLD} MMK")
async def rate_usd(update, context): await update.message.reply_text(f"🇺🇸 1 USD = {USD} MMK")
async def roll_dice(update, context): await update.message.reply_dice()
async def get_info(update, context): await update.message.reply_text(f"🆔 ID: {update.effective_user.id}")
async def get_weather(update, context): await update.message.reply_text("🌡 ရန်ကုန်: 32°C")
async def get_quote(update, context): await update.message.reply_text("💡: အရှုံးမပေးပါနဲ့!")
async def calc(update, context): 
    try: await update.message.reply_text(f"🧮 အဖြေ: {eval(''.join(context.args))}")
    except: await update.message.reply_text("အသုံးပြုပုံ: /calc 10+5")
async def shorten_link(update, context):
    try: await update.message.reply_text(f"🔗: {pyshorteners.Shortener().tinyurl.short(context.args[0])}")
    except: await update.message.reply_text("အသုံးပြုပုံ: /short [link]")
async def generate_qr(update, context):
    try:
        qrcode.make(''.join(context.args)).save('qr.png')
        await update.message.reply_photo(photo=open('qr.png', 'rb'))
    except: await update.message.reply_text("အသုံးပြုပုံ: /qr [စာသား]")
async def gen_pass(update, context):
    length = int(context.args[0]) if context.args else 8
    await update.message.reply_text(f"🔐 Password: {''.join(random.choices(string.ascii_letters, k=length))}")

if __name__ == '__main__':
    Thread(target=run_web).start()
    TOKEN = "8829581045:AAFlpGC-6fPS0UTRZSbAz1ToPz4QusMxiOc"
    app_bot = ApplicationBuilder().token(TOKEN).build()
    
    # ခလုတ်တိုင်းအတွက် Handler များ
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(CommandHandler("help", start))
    app_bot.add_handler(CommandHandler("time", get_time))
    app_bot.add_handler(CommandHandler("rate_gold", rate_gold))
    app_bot.add_handler(CommandHandler("rate_usd", rate_usd))
    app_bot.add_handler(CommandHandler("dice", roll_dice))
    app_bot.add_handler(CommandHandler("info", get_info))
    app_bot.add_handler(CommandHandler("weather", get_weather))
    app_bot.add_handler(CommandHandler("quote", get_quote))
    app_bot.add_handler(CommandHandler("calc", calc))
    app_bot.add_handler(CommandHandler("short", shorten_link))
    app_bot.add_handler(CommandHandler("qr", generate_qr))
    app_bot.add_handler(CommandHandler("pass", gen_pass))
    
    app_bot.run_polling()
    
