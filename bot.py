from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)

TOKEN = "8997612253:AAEKi1LIdvJi7Q8N3tUJY6HXY3S_dUvPIj8"

NAME, NUMBER, GMAIL, PAYMENT = range(4)

GROUP_ID = -1004319616995

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Magacaaga?")
    return NAME

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.message.text
    await update.message.reply_text("Number-kaaga?")
    return NUMBER

async def get_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["number"] = update.message.text
    await update.message.reply_text("Gmail-kaaga?")
    return GMAIL

async def get_gmail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["gmail"] = update.message.text
    await update.message.reply_text("Soo dir sawirka Proof of Payment:")
    return PAYMENT

async def get_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1].file_id

    msg = f"""
NEW REGISTRATION

Name: {context.user_data['name']}
Number: {context.user_data['number']}
Gmail: {context.user_data['gmail']}
"""

    await context.bot.send_photo(
        chat_id=GROUP_ID,
        photo=photo,
        caption=msg
    )

    await update.message.reply_text(
        "Waad ku mahadsan tahay. Xogtaada waa la gudbiyay."
    )

    return ConversationHandler.END

app = Application.builder().token(TOKEN).build()

conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
        NUMBER: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_number)],
        GMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_gmail)],
        PAYMENT: [MessageHandler(filters.PHOTO, get_payment)],
    },
    fallbacks=[],
)

app.add_handler(conv_handler)

print("Bot is running...")
app.run_polling()