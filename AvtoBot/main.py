import re
import time
import os

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

def is_valid_plate(text: str) -> bool:
    pattern = r"^\d{3}[A-Za-z]{3}$"
    return bool(re.match(pattern, text))

def main():
    TOKEN = "8718820157:AAFxzuX1KYZBmdetMT3fKdQF_8CO5atvNHM"

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print("Starting")
    app.run_polling()

if __name__ == "__main__":
    main()
