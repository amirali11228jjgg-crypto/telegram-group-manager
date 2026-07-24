from telegram import Update
from telegram.ext import ContextTypes


async def is_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id
    chat_id = update.effective_chat.id

    admins = await context.bot.get_chat_administrators(chat_id)

    for admin in admins:
        if admin.user.id == user_id:
            return True

    return False


async def require_admin(update, context):

    result = await is_admin(update, context)

    if not result:
        await update.message.reply_text(
            "❌ فقط مدیران گروه می‌توانند از این دستور استفاده کنند."
        )

        return False

    return True
