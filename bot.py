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

# 1. How to register
REGISTER_VIDEO_ID = (
    "BAACAgUAAxkBAAM4arx3ykJH145MNCaXeLBGGfMhCVMAAqcg"
    "AAKwiKlUsUs0MN9Tx2g9BA"
)

# 2. How to deposit
DEPOSIT_VIDEO_ID = (
    "BAACAgUAAxkBAAM6arx4zufS1FRVSM9gVrwAAdZP7rrRAAJsHw"
    "ACeU25VKE3Jomm2mUpPQQ"
)

# 3. How to Withdrawal
WITHDRAWAL_VIDEO_ID = (
    "BAACAgUAAxkBAANbarx8SpyIhpxKImWtpFKNLWlNEfIAAm0f"
    "AAJ5TblU9Bv-JxSlNME9BA"
)

# 4. How to create MT5 Account
MT5_ACCOUNT_VIDEO_ID = (
    "BAACAgUAAxkBAANJarx60H1lnRskXpcK5HtfA934DHEAArse"
    "AAKwiLFUAAHAyjbPw5YVPQQ"
)

# 5. How to create master account
CREATE_MASTER_VIDEO_ID = (
    "BAACAgUAAxkBAAM1arx0zwABszvzJLbgYSQYsMSlIyBH"
    "AAKVIAACdB8JVV_V7FmT0p8rPQQ"
)

# 6. How to copy master account
COPY_MASTER_VIDEO_ID = (
    "BAACAgUAAxkBAANfarx8i3_5E4_zmJcY06BONYqpCMU"
    "AApYgAAJ0HwlV_Ga7QIAab389BA"
)


# =========================================================
# MENU
# =========================================================
MENU = [
    ["How to register"],
    ["How to deposit"],
    ["How to Withdrawal"],
    ["How to create MT5 Account"],
    ["How to create master account"],
    ["How to copy master account"],
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
        "Please select a menu below:",
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
    if text == "How to register":

        await update.message.reply_video(
            video=REGISTER_VIDEO_ID,
            caption=(
                "📱 How to register\n\n"
                "Please watch the video above."
            )
        )

    # =====================================================
    # HOW TO DEPOSIT
    # =====================================================
    elif text == "How to deposit":

        await update.message.reply_video(
            video=DEPOSIT_VIDEO_ID,
            caption=(
                "💰 How to deposit\n\n"
                "Please watch the video above."
            )
        )

    # =====================================================
    # HOW TO WITHDRAWAL
    # =====================================================
    elif text == "How to Withdrawal":

        await update.message.reply_video(
            video=WITHDRAWAL_VIDEO_ID,
            caption=(
                "💸 How to Withdrawal\n\n"
                "Please watch the video above."
            )
        )

    # =====================================================
    # HOW TO CREATE MT5 ACCOUNT
    # =====================================================
    elif text == "How to create MT5 Account":

        await update.message.reply_video(
            video=MT5_ACCOUNT_VIDEO_ID,
            caption=(
                "👤 How to create MT5 Account\n\n"
                "Please watch the video above."
            )
        )

    # =====================================================
    # HOW TO CREATE MASTER ACCOUNT
    # =====================================================
    elif text == "How to create master account":

        await update.message.reply_video(
            video=CREATE_MASTER_VIDEO_ID,
            caption=(
                "⭐ How to create master account\n\n"
                "Please watch the video above."
            )
        )

    # =====================================================
    # HOW TO COPY MASTER ACCOUNT
    # =====================================================
    elif text == "How to copy master account":

        await update.message.reply_video(
            video=COPY_MASTER_VIDEO_ID,
            caption=(
                "📋 How to copy master account\n\n"
                "Please watch the video above."
            )
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
# RUN BOT
# =========================================================
if __name__ == "__main__":
    main()
