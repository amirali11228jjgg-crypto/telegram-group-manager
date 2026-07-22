from telegram import Update
from telegram.ext import ContextTypes

from admin import is_admin
from database import add_warn, get_warns, clear_warns
from config import MAX_WARNS


async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not await is_admin(update):
        return

    if not update.message.reply_to_message:
        await update.message.reply_text(
            "❌ روی پیام کاربر ریپلای کن."
        )
        return

    user = update.message.reply_to_message.from_user

    await update.effective_chat.ban_member(
        user.id
    )

    await update.message.reply_text(
        f"🔨 {user.first_name} بن شد."
    )


async def unban(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not await is_admin(update):
        return

    if not update.message.reply_to_message:
        await update.message.reply_text(
            "❌ روی پیام کاربر ریپلای کن."
        )
        return

    user = update.message.reply_to_message.from_user

    await update.effective_chat.unban_member(
        user.id
    )

    await update.message.reply_text(
        f"✅ {user.first_name} رفع بن شد."
    )


async def kick(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not await is_admin(update):
        return

    if not update.message.reply_to_message:
        await update.message.reply_text(
            "❌ روی پیام کاربر ریپلای کن."
        )
        return

    user = update.message.reply_to_message.from_user

    await update.effective_chat.ban_member(
        user.id
    )

    await update.effective_chat.unban_member(
        user.id
    )

    await update.message.reply_text(
        f"👢 {user.first_name} اخراج شد."
    )


async def warn(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not await is_admin(update):
        return

    if not update.message.reply_to_message:
        await update.message.reply_text(
            "❌ روی پیام کاربر ریپلای کن."
        )
        return

    user = update.message.reply_to_message.from_user

    count = await add_warn(
        update.effective_chat.id,
        user.id
    )

    await update.message.reply_text(
        f"⚠️ {user.first_name} اخطار گرفت\n"
        f"تعداد اخطار: {count}/{MAX_WARNS}"
    )

    if count >= MAX_WARNS:

        await update.effective_chat.ban_member(
            user.id
        )

        await clear_warns(
            update.effective_chat.id,
            user.id
        )

        await update.message.reply_text(
            f"🚫 {user.first_name} به دلیل ۳ اخطار بن شد."
        )
