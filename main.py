import os
from flask import Flask
from threading import Thread
from telegram.ext import ApplicationBuilder, CommandHandler

app = Flask(__name__)
@app.route('/')
def home():
    return "Bot is running!"

def run_web():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

async def start(update, context):
    await update.message.reply_text('Bot အလုပ်လုပ်နေပါပြီ!')

if __name__ == '__main__':
    t = Thread(target=run_web)
    t.start()
    # သင့် Token အစစ်ကို ဒီမှာ ထည့်ထားပြီးသားပါ
    app_bot = ApplicationBuilder().token("8829581045:AAFlpGC-6fPS0UTRZSbAz1ToPz4QusMxiOc").build()
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.run_polling()
  
