from telegram import Update


async def is_admin(update: Update, user_id=None):
    """
    بررسی می‌کند کاربر مدیر گروه هست یا نه
    """

    if not update.effective_chat:
        return False

    # در چت خصوصی مدیر معنی ندارد
    if update.effective_chat.type == "private":
        return False

    if user_id is None:
        user_id = update.effective_user.id

    admins = await update.effective_chat.get_administrators()

    for admin in admins:
        if admin.user.id == user_id:
            return True

    return False


async def admin_only(update: Update):
    """
    محدود کردن دستورها فقط برای ادمین‌ها
    """

    if not await is_admin(update):
        if update.message:
            await update.message.reply_text(
                "⛔ فقط مدیران گروه اجازه استفاده از این دستور را دارند."
            )

        return False

    return True


async def get_admins(update: Update):
    """
    برگرداندن آیدی تمام مدیران گروه
    """

    admins = await update.effective_chat.get_administrators()

    return [
        admin.user.id
        for admin in admins
    ]


async def is_owner(update: Update, user_id=None):
    """
    بررسی مالک اصلی گروه
    """

    if user_id is None:
        user_id = update.effective_user.id

    admins = await update.effective_chat.get_administrators()

    for admin in admins:
        if admin.user.id == user_id:
            return admin.status == "creator"

    return False
