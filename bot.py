import os

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)


TOKEN = os.environ["8991637065:AAGgwgU8irb08L4LcAujjLh76zsSkOTFZnE"]

MENU = [
    ["👉 របៀប Deposit"],
    ["👉 របៀប Withdraw"],
    ["👉 របៀបបញ្ចូល USD Wallet នៅ MT5/MT4"],
    ["👉 របៀបបញ្ចូលគណនី ID MT5/MT4"],
]


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


async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text

    if text == "👉 របៀប Deposit":
        await update.message.reply_text(
            "💰 Deposit\n\n"
            "សូមបញ្ចូលចំនួនទឹកប្រាក់ដែលអ្នកចង់ Deposit។"
        )

    elif text == "👉 របៀប Withdraw":
        await update.message.reply_text(
            "💸 Withdraw\n\n"
            "សូមបញ្ចូលចំនួនទឹកប្រាក់ដែលអ្នកចង់ Withdraw។"
        )

    elif text == "👉 របៀបបញ្ចូល USD Wallet នៅ MT5/MT4":
        await update.message.reply_text(
            "💵 USD Wallet MT5/MT4\n\n"
            "សូមបញ្ចូល USD Wallet របស់អ្នក។"
        )

    elif text == "👉 របៀបបញ្ចូលគណនី ID MT5/MT4":
        await update.message.reply_text(
            "👤 MT5/MT4 Account ID\n\n"
            "សូមបញ្ចូល Account ID របស់អ្នក។"
        )


def main():

    port = int(os.environ.get("PORT", "10000"))
    render_url = os.environ.get("RENDER_EXTERNAL_URL")

    if not render_url:
        raise RuntimeError(
            "RENDER_EXTERNAL_URL is not available. "
            "This bot is configured for Render."
        )

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            menu
        )
    )

    print("Bot is starting with webhook...")

    app.run_webhook(
        listen="0.0.0.0",
        port=port,
        webhook_url=f"{render_url}/telegram",
        url_path="telegram",
        drop_pending_updates=True,
    )


if __name__ == "__main__":
    main()