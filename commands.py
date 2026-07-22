from telegram import Update, ChatPermissions
from telegram.ext import ContextTypes

from admin import admin_only
from database import (
    add_warning,
    get_warnings,
    clear_warnings,
    add_log
)

from config import MAX_WARNINGS


async def warn(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not await admin_only(update):
        return

    if not update.message.reply_to_message:
        await update.message.reply_text(
            "⚠️ روی پیام کاربر ریپلای کنید."
        )
        return

    target = update.message.reply_to_message.from_user
    chat_id = update.effective_chat.id

    await add_warning(target.id, chat_id)

    count = await get_warnings(target.id, chat_id)

    await add_log(
        chat_id,
        update.effective_user.id,
        "warn",
        target.id
    )

    if count >= MAX_WARNINGS:

        await update.effective_chat.ban_member(
            target.id
        )

        await clear_warnings(
            target.id,
            chat_id
        )

        await update.message.reply_text(
            f"🚫 {target.first_name} به دلیل سه اخطار بن شد."
        )

    else:
        await update.message.reply_text(
            f"⚠️ اخطار ثبت شد\n"
            f"تعداد اخطار: {count}/{MAX_WARNINGS}"
        )


async def warnings(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not update.message.reply_to_message:
        await update.message.reply_text(
            "⚠️ روی پیام کاربر ریپلای کنید."
        )
        return

    target = update.message.reply_to_message.from_user

    count = await get_warnings(
        target.id,
        update.effective_chat.id
    )

    await update.message.reply_text(
        f"📌 اخطارهای {target.first_name}: {count}"
    )


async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not await admin_only(update):
        return

    if not update.message.reply_to_message:
        return

    target = update.message.reply_to_message.from_user

    await update.effective_chat.ban_member(
        target.id
    )

    await add_log(
        update.effective_chat.id,
        update.effective_user.id,
        "ban",
        target.id
    )

    await update.message.reply_text(
        f"🚫 {target.first_name} بن شد."
    )


async def kick(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not await admin_only(update):
        return

    if not update.message.reply_to_message:
        return

    target = update.message.reply_to_message.from_user

    await update.effective_chat.ban_member(target.id)
    await update.effective_chat.unban_member(target.id)

    await update.message.reply_text(
        f"👢 {target.first_name} حذف شد."
    )


async def mute(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not await admin_only(update):
        return

    if not update.message.reply_to_message:
        return

    target = update.message.reply_to_message.from_user

    permissions = ChatPermissions(
        can_send_messages=False
    )

    await update.effective_chat.restrict_member(
        target.id,
        permissions
    )

    await update.message.reply_text(
        f"🔇 {target.first_name} سکوت شد."
    )


async def unmute(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not await admin_only(update):
        return

    if not update.message.reply_to_message:
        return

    target = update.message.reply_to_message.from_user

    permissions = ChatPermissions(
        can_send_messages=True
    )

    await update.effective_chat.restrict_member(
        target.id,
        permissions
    )

    await update.message.reply_text(
        f"🔊 {target.first_name} رفع سکوت شد."
    async def unban(update, context):
    if update.message.reply_to_message:
        user = update.message.reply_to_message.from_user

        await update.effective_chat.unban_member(
            user.id
        )

        await update.message.reply_text(
            f"✅ {user.first_name} رفع بن شد."
        )
    else:
        await update.message.reply_text(
            "❌ روی پیام کاربر ریپلای کن."
        )
