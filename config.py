import os
from dotenv import load_dotenv

# خواندن متغیرهای محیطی
load_dotenv()

# توکن ربات تلگرام
BOT_TOKEN = os.getenv("BOT_TOKEN")

# تنظیمات اصلی ربات

# تعداد اخطار مجاز قبل از بن خودکار
MAX_WARNINGS = 3

# دیتابیس
DATABASE_NAME = "bot_database.db"

# تنظیمات حذف لینک
LINK_FILTER_ENABLED = True

# تنظیمات لاگ
LOG_ENABLED = True


def get_config():
    """
    نمایش تنظیمات فعلی
    """
    return {
        "max_warnings": MAX_WARNINGS,
        "database": DATABASE_NAME,
        "link_filter": LINK_FILTER_ENABLED,
        "logging": LOG_ENABLED
    }
