import logging
import asyncio

from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters
)

from config import BOT_TOKEN

from database import init_db

from commands import (
    warn,
    warnings,
    ban,
    kick,
    mute,
    unmute
)

from filters import (
    delete_links,
    word_filter
)


logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)


async def start(update, context):

    await update.message.reply_text(
        "🤖 ربات مدیریت گروه فعال شد."
    )


def main():

    # ساخت دیتابیس
    asyncio.run(init_db())


    # ساخت ربات
    app = Application.builder().token(
        BOT_TOKEN
    ).build()


    # دستورات

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        CommandHandler("warn", warn)
    )

    app.add_handler(
        CommandHandler("warnings", warnings)
    )

    app.add_handler(
        CommandHandler("ban", ban)
    )

    app.add_handler(
        CommandHandler("kick", kick)
    )

    app.add_handler(
        CommandHandler("mute", mute)
    )

    app.add_handler(
        CommandHandler("unmute", unmute)
    )


    # فیلتر پیام‌ها

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            delete_links
        )
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            word_filter
        )
    )


    print("Bot started...")


    # اجرای ربات
    app.run_polling()



if __name__ == "__main__":
    main()
