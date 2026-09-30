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
TOKEN = os.environ["BOT_TOKEN"]


# =========================================================
# VIDEO FILE IDs
# =========================================================

# How to Register video
REGISTER_VIDEO_ID = (
    "BAACAgUAAxkBAAM4arx3ykJH145MNCaXeLBGGfMhCVMAAqcg"
    "AAKwiKlUsUs0MN9Tx2g9BA"
)

# Add the other video File IDs here later
DEPOSIT_VIDEO_ID = None
WITHDRAWAL_VIDEO_ID = None
MT5_VIDEO_ID = None


# =========================================================
# MENU
# =========================================================
MENU = [
    ["How to Register"],
    ["How to deposit"],
    ["How to Withdrawal"],
    ["How to create MT5 Account"],
]


# =========================================================
# /start
# =========================================================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = ReplyKeyboardMarkup(
        MENU,
        resize_keyboard=True
    )

    await update.message.reply_text(
        "សូមស្វាគមន៍មកកាន់ LX Cambodia 🇰🇭\n\n"
        "Please select a menu:",
        reply_markup=keyboard
    )


# =========================================================
# MENU HANDLER
# =========================================================
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text

    # =====================================================
    # HOW TO REGISTER
    # =====================================================
    if text == "How to Register":

        await update.message.reply_video(
            video=REGISTER_VIDEO_ID,
            caption=(
                "📱 How to Register\n\n"
                "Please watch the video above."
            )
        )

    # =====================================================
    # HOW TO DEPOSIT
    # =====================================================
    elif text == "How to deposit":

        if DEPOSIT_VIDEO_ID:

            await update.message.reply_video(
                video=DEPOSIT_VIDEO_ID,
                caption=(
                    "💰 How to deposit\n\n"
                    "Please watch the video above."
                )
            )

        else:

            await update.message.reply_text(
                "💰 How to deposit\n\n"
                "Deposit video will be available soon."
            )

    # =====================================================
    # HOW TO WITHDRAWAL
    # =====================================================
    elif text == "How to Withdrawal":

        if WITHDRAWAL_VIDEO_ID:

            await update.message.reply_video(
                video=WITHDRAWAL_VIDEO_ID,
                caption=(
                    "💸 How to Withdrawal\n\n"
                    "Please watch the video above."
                )
            )

        else:

            await update.message.reply_text(
                "💸 How to Withdrawal\n\n"
                "Withdrawal video will be available soon."
            )

    # =====================================================
    # HOW TO CREATE MT5 ACCOUNT
    # =====================================================
    elif text == "How to create MT5 Account":

        if MT5_VIDEO_ID:

            await update.message.reply_video(
                video=MT5_VIDEO_ID,
                caption=(
                    "👤 How to create MT5 Account\n\n"
                    "Please watch the video above."
                )
            )

        else:

            await update.message.reply_text(
                "👤 How to create MT5 Account\n\n"
                "MT5 Account video will be available soon."
            )


# =========================================================
# MAIN
# =========================================================
def main():

    # Render PORT
    port = int(
        os.environ.get("PORT", "10000")
    )

    # Render public URL
    render_url = os.environ.get(
        "RENDER_EXTERNAL_URL"
    )

    if not render_url:

        raise RuntimeError(
            "RENDER_EXTERNAL_URL is not available. "
            "This bot is configured for Render."
        )

    # =====================================================
    # TELEGRAM HTTP REQUEST
    # =====================================================
    request = HTTPXRequest(
        connect_timeout=60,
        read_timeout=60,
        write_timeout=60,
        pool_timeout=60,
    )

    # =====================================================
    # CREATE APPLICATION
    # =====================================================
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

    # Menu buttons
    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            menu
        )
    )

    # =====================================================
    # START WEBHOOK
    # =====================================================
    print("========================================")
    print("LX Cambodia Telegram Bot")
    print("Bot is starting with webhook...")
    print(f"Port: {port}")
    print(f"Webhook: {render_url}/telegram")
    print("========================================")

    app.run_webhook(
        listen="0.0.0.0",
        port=port,
        url_path="telegram",
        webhook_url=f"{render_url}/telegram",
        drop_pending_updates=True,
    )


# =========================================================
# RUN
# =========================================================
if __name__ == "__main__":
    main()
