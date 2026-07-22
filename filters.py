from telegram import Update
from telegram.ext import ContextTypes
from config import LINK_FILTER


def contains_link(text: str) -> bool:
    if not text:
        return False

    links = [
        "http://",
        "https://",
        "t.me/",
        "www."
    ]

    return any(link in text.lower() for link in links)


async def link_filter(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not LINK_FILTER:
        return

    if not update.message:
        return

    text = update.message.text

    if contains_link(text):

        try:
            await update.message.delete()

            await update.effective_chat.send_message(
                "🚫 ارسال لینک در این گروه مجاز نیست."
            )

        except Exception:
            pass
