from telegram import Update
from telegram.ext import ContextTypes


# کلمات یا لینک‌هایی که می‌خواهیم بررسی کنیم
LINK_WORDS = [
    "http://",
    "https://",
    "www.",
    ".com",
    ".ir",
    ".net",
    ".org"
]


async def link_filter(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not update.message:
        return

    text = update.message.text

    if not text:
        return

    text = text.lower()

    for word in LINK_WORDS:

        if word in text:

            try:
                await update.message.delete()

                await update.message.chat.send_message(
                    "🚫 ارسال لینک در این گروه مجاز نیست."
                )

            except Exception:
                pass

            return
