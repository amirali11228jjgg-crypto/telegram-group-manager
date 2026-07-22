from telegram import Update
from telegram.ext import ContextTypes

from config import LINK_FILTER_ENABLED


async def delete_links(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not LINK_FILTER_ENABLED:
        return

    if not update.message:
        return

    text = update.message.text

    if not text:
        return

    links = [
        "http://",
        "https://",
        "www.",
        "t.me/"
    ]

    for link in links:
        if link in text.lower():

            try:
                await update.message.delete()

                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=(
                        "🚫 ارسال لینک در این گروه مجاز نیست."
                    )
                )

            except Exception:
                pass

            break


async def word_filter(update: Update, context: ContextTypes.DEFAULT_TYPE):

    """
    فیلتر کلمات
    (فعلاً آماده برای توسعه نسخه بعد)
    """

    blocked_words = [
        # کلمات ممنوعه بعداً اضافه می‌شوند
    ]

    if not update.message or not update.message.text:
        return

    text = update.message.text.lower()

    for word in blocked_words:
        if word in text:

            await update.message.delete()

            break
