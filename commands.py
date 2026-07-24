from telegram import Update
from telegram.ext import ContextTypes

from permissions import require_admin
from database import add_warning, get_warnings, clear_warnings


async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not await require_admin(update, context):
        return

    if not update.message.reply_to_message:
        await update.message.reply_text(
            "❌ روی پیام کاربر ریپلای کنید."
        )
        return

    user = update.message.reply_to_message.from_user

    await context.bot.ban_chat_member(
        update.effective_chat.id,
        user.id
    )

    await update.message.reply_text(
        f"🚫 {user.first_name} از گروه بن شد."
    )


async def unban(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not await require_admin(update, context):
        return

    if not context.args:
        await update.message.reply_text(
            "استفاده: /unban USER_ID"
        )
        return

    user_id = int(context.args[0])

    await context.bot.unban_chat_member(
        update.effective_chat.id,
        user_id
    )

    await update.message.reply_text(
        "✅ کاربر آزاد شد."
    )


async def kick(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not await require_admin(update, context):
        return

    if not update.message.reply_to_message:
        await update.message.reply_text(
            "❌ روی پیام کاربر ریپلای کنید."
        )
        return

    user = update.message.reply_to_message.from_user

    await context.bot.ban_chat_member(
        update.effective_chat.id,
        user.id
    )

    await context.bot.unban_chat_member(
        update.effective_chat.id,
        user.id
    )

    await update.message.reply_text(
        f"👢 {user.first_name} اخراج شد."
    )


async def mute(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not await require_admin(update, context):
        return

    if not update.message.reply_to_message:
        await update.message.reply_text(
            "❌ روی پیام کاربر ریپلای کنید."
        )
        return

    user = update.message.reply_to_message.from_user

    await context.bot.restrict_chat_member(
        update.effective_chat.id,
        user.id,
        permissions={
            "can_send_messages": False
        }
    )

    await update.message.reply_text(
        f"🔇 {user.first_name} میوت شد."
    )


async def unmute(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not await require_admin(update, context):
        return

    if not update.message.reply_to_message:
        return

    user = update.message.reply_to_message.from_user

    await context.bot.restrict_chat_member(
        update.effective_chat.id,
        user.id,
        permissions={
            "can_send_messages": True
        }
    )

    await update.message.reply_text(
        f"🔊 {user.first_name} آزاد شد."
    )


async def warn(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not await require_admin(update, context):
        return

    if not update.message.reply_to_message:
        await update.message.reply_text(
            "❌ روی پیام کاربر ریپلای کنید."
        )
        return

    user = update.message.reply_to_message.from_user

    reason = " ".join(context.args)

    if not reason:
        reason = "بدون دلیل"

    await add_warning(
        user.id,
        user.username,
        reason,
        update.effective_user.id
    )

    await update.message.reply_text(
        f"⚠️ {user.first_name} اخطار گرفت."
    )


async def warnings(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not update.message.reply_to_message:
        await update.message.reply_text(
            "❌ روی پیام کاربر ریپلای کنید."
        )
        return

    user = update.message.reply_to_message.from_user

    data = await get_warnings(user.id)

    if not data:
        await update.message.reply_text(
            "✅ هیچ اخطاری ندارد."
        )
        return

    text = "⚠️ اخطارها:\n\n"

    for reason, date in data:
        text += f"• {reason} ({date})\n"

    await update.message.reply_text(text)
