from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatMemberStatus


async def is_admin(update: Update) -> bool:
    """بررسی می‌کند ارسال‌کننده پیام ادمین یا مالک گروه باشد."""

    if update.effective_chat is None or update.effective_user is None:
        return False

    member = await update.effective_chat.get_member(
        update.effective_user.id
    )

    return member.status in (
        ChatMemberStatus.OWNER,
        ChatMemberStatus.ADMINISTRATOR,
    )


async def admin_only(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    اگر کاربر ادمین نباشد True برمی‌گرداند
    تا هندلر ادامه پیدا نکند.
    """

    if not await is_admin(update):
        if update.message:
            await update.message.reply_text(
                "⛔ فقط مدیران گروه می‌توانند از این دستور استفاده کنند."
            )
        return True

    return False
