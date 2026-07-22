import logging

from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
)

from config import BOT_TOKEN

from database import init_db

from commands import (
    ban,
    unban,
    kick,
    warn,
    mute,
    unmute,
    warnings,
)

from filters import link_filter


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)


async def start(update, context):

    await update.message.reply_text(
        "🤖 ربات مدیریت گروه فعال شد."
    )


async def setup(app):

    await init_db()


def main():

    app = Application.builder().token(
        BOT_TOKEN
    ).post_init(
        setup
    ).build()


    # دستورات انگلیسی

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        CommandHandler("ban", ban)
    )

    app.add_handler(
        CommandHandler("unban", unban)
    )

    app.add_handler(
        CommandHandler("kick", kick)
    )

    app.add_handler(
        CommandHandler("warn", warn)
    )

    app.add_handler(
        CommandHandler("mute", mute)
    )

    app.add_handler(
        CommandHandler("unmute", unmute)
    )

    app.add_handler(
        CommandHandler("warnings", warnings)
    )


    # حذف لینک

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            link_filter
        )
    )


    print("Bot started...")

    app.run_polling()


if __name__ == "__main__":
    main()
