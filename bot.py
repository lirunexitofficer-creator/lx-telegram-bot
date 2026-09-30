import os

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from telegram.request import HTTPXRequest


# =========================================================
# BOT TOKEN
# =========================================================
# Render Environment Variable:
# BOT_TOKEN = your Telegram Bot Token
TOKEN = os.environ["BOT_TOKEN"]


# =========================================================
# MENU
# =========================================================
MENU = [
    ["👉 របៀប Deposit"],
    ["👉 របៀប Withdraw"],
    ["👉 របៀបបញ្ចូល USD Wallet នៅ MT5/MT4"],
    ["👉 របៀបបញ្ចូលគណនី ID MT5/MT4"],
]


# =========================================================
# START COMMAND
# =========================================================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = ReplyKeyboardMarkup(
        MENU,
        resize_keyboard=True
    )

    await update.message.reply_text(
        "សូមស្វាគមន៍មកកាន់ LX Cambodia 🇰🇭\n\n"
        "សូមជ្រើសរើស Menu ខាងក្រោម៖",
        reply_markup=keyboard
    )


# =========================================================
# VIDEO FILE ID
# =========================================================
async def get_video_id(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.message and update.message.video:

        file_id = update.message.video.file_id

        await update.message.reply_text(
            "✅ Video received!\n\n"
            "📌 Video File ID:\n\n"
            f"{file_id}\n\n"
            "Copy this File ID and keep it safe."
        )


# =========================================================
# MENU HANDLER
# =========================================================
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text

    # -----------------------------------------------------
    # DEPOSIT
    # -----------------------------------------------------
    if text == "👉 របៀប Deposit":

        await update.message.reply_text(
            "💰 Deposit\n\n"
            "សូមបញ្ចូលចំនួនទឹកប្រាក់ដែលអ្នកចង់ Deposit។"
        )

    # -----------------------------------------------------
    # WITHDRAW
    # -----------------------------------------------------
    elif text == "👉 របៀប Withdraw":

        await update.message.reply_text(
            "💸 Withdraw\n\n"
            "សូមបញ្ចូលចំនួនទឹកប្រាក់ដែលអ្នកចង់ Withdraw។"
        )

    # -----------------------------------------------------
    # USD WALLET
    # -----------------------------------------------------
    elif text == "👉 របៀបបញ្ចូល USD Wallet នៅ MT5/MT4":

        await update.message.reply_text(
            "💵 USD Wallet MT5/MT4\n\n"
            "សូមបញ្ចូល USD Wallet របស់អ្នក។"
        )

    # -----------------------------------------------------
    # MT5 / MT4 ACCOUNT ID
    # -----------------------------------------------------
    elif text == "👉 របៀបបញ្ចូលគណនី ID MT5/MT4":

        await update.message.reply_text(
            "👤 MT5/MT4 Account ID\n\n"
            "សូមបញ្ចូល Account ID របស់អ្នក។"
        )


# =========================================================
# MAIN
# =========================================================
def main():

    # -----------------------------------------------------
    # RENDER PORT
    # -----------------------------------------------------
    port = int(
        os.environ.get("PORT", "10000")
    )

    # -----------------------------------------------------
    # RENDER PUBLIC URL
    # -----------------------------------------------------
    render_url = os.environ.get(
        "RENDER_EXTERNAL_URL"
    )

    if not render_url:

        raise RuntimeError(
            "RENDER_EXTERNAL_URL is not available. "
            "This bot is configured for Render."
        )

    # -----------------------------------------------------
    # TELEGRAM HTTP REQUEST
    # -----------------------------------------------------
    request = HTTPXRequest(
        connect_timeout=60,
        read_timeout=60,
        write_timeout=60,
        pool_timeout=60,
    )

    # -----------------------------------------------------
    # CREATE APPLICATION
    # -----------------------------------------------------
    app = (
        Application.builder()
        .token(TOKEN)
        .request(request)
        .build()
    )

    # =====================================================
    # HANDLERS
    # =====================================================

    # /start
    app.add_handler(
        CommandHandler(
            "start",
            start
        )
    )

    # Video handler
    # Sending a video to the bot will return its File ID.
    app.add_handler(
        MessageHandler(
            filters.VIDEO,
            get_video_id
        )
    )

    # Text / menu handler
    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            menu
        )
    )

    # -----------------------------------------------------
    # START MESSAGE
    # -----------------------------------------------------
    print("========================================")
    print("LX Cambodia Telegram Bot")
    print("Bot is starting with webhook...")
    print(f"Port: {port}")
    print(f"Webhook: {render_url}/telegram")
    print("========================================")

    # -----------------------------------------------------
    # START WEBHOOK
    # -----------------------------------------------------
    app.run_webhook(
        listen="0.0.0.0",
        port=port,
        url_path="telegram",
        webhook_url=f"{render_url}/telegram",
        drop_pending_updates=True,
    )


# =========================================================
# RUN BOT
# =========================================================
if __name__ == "__main__":
    main()
