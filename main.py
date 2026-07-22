from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters
)
from telegram.error import TelegramError

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
        "/help - راهنما\n"
        "/بن یا /ban - بن کردن با ریپلای"
    )


async def ban_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        await update.message.reply_text(
            "❌ روی پیام کاربر ریپلای کن و بعد بن را بزن"
        )
        return

    user = update.message.reply_to_message.from_user

    try:
        await context.bot.ban_chat_member(
            chat_id=update.effective_chat.id,
            user_id=user.id
        )

        await update.message.reply_text(
            f"🚫 {user.first_name} بن شد."
        )

    except TelegramError:
        await update.message.reply_text(
            "❌ نتوانستم کاربر را بن کنم."
        )


async def delete_links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.text:
        if "http" in update.message.text:
            await update.message.delete()


async def text_ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text in ["بن", "ban"]:
        await ban_user(update, context)


def main():
    create_tables()

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))

    # دستورات /بن و /ban
    app.add_handler(CommandHandler("بن", ban_user))
    app.add_handler(CommandHandler("ban", ban_user))

    # بن بدون /
    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            text_ban
        )
    )

    # حذف لینک
    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            delete_links
        )
    )

    print("Bot is running...")

    app.run_polling()


if __name__ == "__main__":
    main()
