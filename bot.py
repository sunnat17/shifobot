# Bot fayli: bot.py
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

def start(update: Update, context: CallbackContext):
    keyboard = [
        ["👨‍⚕️ Врач танлаш"],
        ["📅 Қабулга ёзилиш"],
        ["💳 Тўлов қилиш"],
        ["🏥 Клиника ҳақида маълумот"],
        ["📞 Биз билан боғланиш"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_text(
        "Ассалому алайкум! 👨‍⚕️\nШифоNur клиникаси ботига хуш келибсиз!\nҚуйидаги менюдан танланг:",
        reply_markup=reply_markup
    )

def handle_message(update: Update, context: CallbackContext):
    text = update.message.text

    if text == "👨‍⚕️ Врач танлаш":
        doctors_keyboard = [["👨‍⚕️ Терапевт"], ["🏥 Гинеколог"], ["🧒 Педиатр"], ["🧠 Психолог"], ["⬅️ Асосий менюга қайтиш"]]
        reply_markup = ReplyKeyboardMarkup(doctors_keyboard, resize_keyboard=True)
        update.message.reply_text("Қуйида врачларни танланг:", reply_markup=reply_markup)

    elif text in ["👨‍⚕️ Терапевт", "🏥 Гинеколог", "🧒 Педиатр", "🧠 Психолог"]:
        update.message.reply_text(f"{text} ҳақида маълумот: Бизда тажрибали {text.lower()} хизмат кўрсатади.")

    elif text == "📅 Қабулга ёзилиш":
        update.message.reply_text("Қабулга ёзилиш учун қўнғироқ қилинг: 📞 +998 90 123 45 67")

    elif text == "💳 Тўлов қилиш":
        update.message.reply_text("Тўлов тизимлари: Click, Payme, Uzum Pay орқали амалга оширишингиз мумкин.")

    elif text == "🏥 Клиника ҳақида маълумот":
        update.message.reply_text("ШифоNur клиникаси — замонавий диагностика ва даволаш маркази.")

    elif text == "📞 Биз билан боғланиш":
        update.message.reply_text("Биз билан боғланиш учун: 📞 +998 90 123 45 67")

    elif text == "⬅️ Асосий менюга қайтиш":
        start(update, context)

    elif text.startswith("/help"):
        context.bot.send_message(chat_id="@Sunnatillo_17", text=f"Фойдаланувчи қуйидаги ёрдам сўровини юборди: {text}")
        update.message.reply_text("Ёрдам сўровингиз админга юборилди, тез орада жавоб берамиз!")

    else:
        update.message.reply_text("Илтимос, менюдан бирини танланг ёки /start буйруғини босинг.")

def main():
    updater = Updater("7563405005:AAFN2Xu5H4AHfu7ycAkUIXvRDzMd0EBsC3Q", use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", handle_message))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

# # requirements.txt
# python-telegram-bot==13.15

# # README.md
# # ShifoBot
# Bu loyihada Telegram bot kodlari joylashgan.

# ## Ishga tushirish:
# ```
# pip install -r requirements.txt
# python bot.py
# ```

# ## Render.com deploy qilish:
# - GitHub’ga yuklang
# - Render.com’dan Web Service qilib ulang
# - Build Command: `pip install -r requirements.txt`
# - Start Command: `python bot.py`

# ✅ Tayyor! Bot doimiy ishlaydi!

#7563405005:AAFN2Xu5H4AHfu7ycAkUIXvRDzMd0EBsC3Q
