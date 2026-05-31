import os, random, qrcode, string, pyshorteners, logging
from datetime import datetime
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler

# Logging စနစ်
logging.basicConfig(level=logging.INFO)

# Main Menu ခလုတ်များ
def get_main_menu():
    keyboard = [
        [InlineKeyboardButton("🌟 ရွှေဈေး", callback_data='gold'), InlineKeyboardButton("🇺🇸 ဒေါ်လာဈေး", callback_data='usd')],
        [InlineKeyboardButton("🧮 တွက်ချက်ရန်", callback_data='calc_help'), InlineKeyboardButton("🎲 အန်စာတုံး", callback_data='dice')],
        [InlineKeyboardButton("🔗 လင့်ခ်အတို", callback_data='short_help'), InlineKeyboardButton("🔐 Password", callback_data='pass_help')],
        [InlineKeyboardButton("⏰ အချိန်/ID", callback_data='info'), InlineKeyboardButton("🖼 QR Code", callback_data='qr_help')]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context):
    await update.message.reply_text("👋 မင်္ဂလာပါ! ကျွန်တော်က အများသုံး Helper Bot ပါ။ အောက်ပါ Menu များမှ ရွေးချယ်နိုင်ပါသည်။", reply_markup=get_main_menu())

async def button_click(update: Update, context):
    query = update.callback_query
    await query.answer()
    back_btn = [[InlineKeyboardButton("🔙 Back", callback_data='back')]]
    
    if query.data == 'gold': await query.edit_message_text("🌟 ရွှေဈေး (၁ ကျပ်သား) = 5,800,000 MMK", reply_markup=InlineKeyboardMarkup(back_btn))
    elif query.data == 'usd': await query.edit_message_text("🇺🇸 ဒေါ်လာဈေး (၁ ဒေါ်လာ) = 4,850 MMK", reply_markup=InlineKeyboardMarkup(back_btn))
    elif query.data == 'info': await query.edit_message_text(f"🆔 သင့် ID: {query.from_user.id}\n⏰ အချိန်: {datetime.now().strftime('%H:%M:%S')}", reply_markup=InlineKeyboardMarkup(back_btn))
    elif query.data == 'dice': 
        await context.bot.send_dice(chat_id=query.message.chat_id)
        await query.edit_message_text("🎲 အန်စာတုံး လှိမ့်ပြီးပါပြီ!", reply_markup=InlineKeyboardMarkup(back_btn))
    elif query.data == 'back': await query.edit_message_text("👋 ဘာများကူညီပေးရမလဲ။", reply_markup=get_main_menu())
    else: 
        help_guides = {
            'calc_help': "🧮 တွက်ရန်: /calc 10+5",
            'short_help': "🔗 လင့်ခ်: /short [link]",
            'pass_help': "🔐 Password: /pass [length]",
            'qr_help': "🖼 QR Code: /qr [text]"
        }
        await query.edit_message_text(help_guides.get(query.data, "လုပ်ဆောင်ချက်အသစ်"), reply_markup=InlineKeyboardMarkup(back_btn))

# Command လုပ်ဆောင်ချက်များ
async def calc(update, context): 
    try: await update.message.reply_text(f"🧮 အဖြေ: {eval(''.join(context.args))}")
    except: await update.message.reply_text("အသုံးပြုပုံ: /calc 10+5")

async def short(update, context):
    try: await update.message.reply_text(f"🔗 လင့်ခ်အတို: {pyshorteners.Shortener().tinyurl.short(context.args[0])}")
    except: await update.message.reply_text("အသုံးပြုပုံ: /short [link]")

async def pass_gen(update, context):
    length = int(context.args[0]) if context.args else 8
    password = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    await update.message.reply_text(f"🔐 Password: {password}")

async def qr_gen(update, context):
    try:
        qrcode.make(''.join(context.args)).save('qr.png')
        await update.message.reply_photo(photo=open('qr.png', 'rb'))
    except: await update.message.reply_text("အသုံးပြုပုံ: /qr [စာသား]")

if __name__ == '__main__':
    # Token အသစ်ကို ဒီနေရာမှာ ထည့်ပေးထားပါတယ်
    TOKEN = "8979386653:AAGSvR5bYIzixafDXsmVNFVZ93uNa0o-xRs"
    app_bot = ApplicationBuilder().token(TOKEN).build()
    
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(CommandHandler("calc", calc))
    app_bot.add_handler(CommandHandler("short", short))
    app_bot.add_handler(CommandHandler("pass", pass_gen))
    app_bot.add_handler(CommandHandler("qr", qr_gen))
    app_bot.add_handler(CallbackQueryHandler(button_click))
    
    print("Bot စတင်လည်ပတ်နေပါပြီ...")
    app_bot.run_polling()
