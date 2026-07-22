from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters
)

from config import BOT_TOKEN
from database import create_tables


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام 👋\nربات محافظ گروه فعال شد 🛡️"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "دستورات ربات:\n\n"
        "/start - فعال بودن ربات\n"
        "/help - راهنما"
    )


async def delete_links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and "http" in update.message.text:
        await update.message.delete()


def main():
    create_tables()

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))

    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, delete_links)
    )

    print("Bot is running...")

    app.run_polling()


if __name__ == "__main__":
    main()
