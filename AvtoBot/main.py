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

def calculate_tax(engine_volume: float) -> int:
    if engine_volume <= 0 or engine_volume > 10:
        return -1

    if engine_volume <= 1.1:
        return 1 * MPR
    elif engine_volume <= 1.5:
        return 2 * MPR
    elif engine_volume <= 2:
        return 3 * MPR
    elif engine_volume <= 2.5:
        return 6 * MPR
    elif engine_volume <= 3:
        return 9 * MPR
    elif engine_volume <= 4:
        return 15 * MPR
    else:
        return 117 * MPR

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
