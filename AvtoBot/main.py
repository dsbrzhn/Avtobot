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

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

def check_plate(number: str) -> str:
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 10)

    try:
        driver.get(URL)

        digits = number[:3]
        letters = number[3:6]

        num_input = wait.until(EC.presence_of_element_located((By.ID, "num")))
        ser_input = wait.until(EC.presence_of_element_located((By.ID, "ser")))

        num_input.clear()
        num_input.send_keys(digits)

        ser_input.clear()
        ser_input.send_keys(letters)

        price_el = wait.until(EC.visibility_of_element_located((By.ID, "price")))

        time.sleep(2)

        return price_el.text

    finally:
        driver.quit()

def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🚗 Plate Number", callback_data="plate")],
        [InlineKeyboardButton("🧾 Tax", callback_data="tax")],
        [InlineKeyboardButton("🛑 Stop", callback_data="stop")],
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()

    await update.message.reply_text(
        "How can I assist you?:",
        reply_markup=main_menu()

    async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "plate":
        context.user_data["mode"] = "plate"
        await query.message.reply_text("Enter plate number (example: 123BDA)")

    elif query.data == "tax":
        context.user_data["mode"] = "tax"
        await query.message.reply_text("Enter engine displacement (example: 2.0)")

    elif query.data == "stop":
        context.user_data.clear()

        await query.message.reply_text("💀 Shutting down")

        os._exit(0)

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    mode = context.user_data.get("mode")

    if not mode:
        await update.message.reply_text(
            "Chose function",
            reply_markup=main_menu()
        )
        return

    if mode == "plate":

        if not is_valid_plate(text):
            await update.message.reply_text("❌ Incorrect format (123BDA)")
            return

        await update.message.reply_text("⏳ Please wait")

        try:
            price = check_plate(text)

            await update.message.reply_text(
                f"💰 Price of plate number: {price} ₸",
                reply_markup=main_menu()
            )

        except Exception as e:
            await update.message.reply_text(f"❌ Error: {str(e)}")

    elif mode == "tax":

        try:
            volume = float(text)
        except ValueError:
            await update.message.reply_text("❌ Enter float (example 2.0)")
            return

        tax = calculate_tax(volume)

        if tax == -1:
            await update.message.reply_text("❌ Incorrect displacement (0.1 - 10)")
            return

        await update.message.reply_text(
            f"🧾 Tax: {tax} ₸",
            reply_markup=main_menu()
        )

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
