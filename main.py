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
    unmute,
    unban
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


async def setup(application):
    await init_db()


def main():

    app = (
        Application.builder()
        .token(BOT_TOKEN)
        .post_init(setup)
        .build()
    )


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


    app.run_polling()


if __name__ == "__main__":
    main()
