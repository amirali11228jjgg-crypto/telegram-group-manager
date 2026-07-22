import aiosqlite
from config import DATABASE_NAME


async def init_db():
    """
    ساخت دیتابیس و جدول‌ها
    """
    async with aiosqlite.connect(DATABASE_NAME) as db:

        # جدول کاربران و اخطارها
        await db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER,
            chat_id INTEGER,
            warnings INTEGER DEFAULT 0,
            PRIMARY KEY(user_id, chat_id)
        )
        """)

        # جدول سکوت کاربران
        await db.execute("""
        CREATE TABLE IF NOT EXISTS mutes (
            user_id INTEGER,
            chat_id INTEGER,
            until_time TEXT,
            PRIMARY KEY(user_id, chat_id)
        )
        """)

        # جدول لاگ مدیریت
        await db.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER,
            admin_id INTEGER,
            action TEXT,
            target_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        await db.commit()


async def add_warning(user_id, chat_id):
    """
    اضافه کردن یک اخطار
    """
    async with aiosqlite.connect(DATABASE_NAME) as db:

        await db.execute("""
        INSERT INTO users(user_id, chat_id, warnings)
        VALUES (?, ?, 1)
        ON CONFLICT(user_id, chat_id)
        DO UPDATE SET warnings = warnings + 1
        """, (user_id, chat_id))

        await db.commit()


async def get_warnings(user_id, chat_id):
    """
    گرفتن تعداد اخطارها
    """
    async with aiosqlite.connect(DATABASE_NAME) as db:

        cursor = await db.execute("""
        SELECT warnings FROM users
        WHERE user_id=? AND chat_id=?
        """, (user_id, chat_id))

        result = await cursor.fetchone()

        return result[0] if result else 0


async def clear_warnings(user_id, chat_id):
    """
    پاک کردن اخطارها
    """
    async with aiosqlite.connect(DATABASE_NAME) as db:

        await db.execute("""
        UPDATE users
        SET warnings=0
        WHERE user_id=? AND chat_id=?
        """, (user_id, chat_id))

        await db.commit()


async def add_log(chat_id, admin_id, action, target_id):
    """
    ثبت عملیات مدیر
    """
    async with aiosqlite.connect(DATABASE_NAME) as db:

        await db.execute("""
        INSERT INTO logs(chat_id, admin_id, action, target_id)
        VALUES (?, ?, ?, ?)
        """, (chat_id, admin_id, action, target_id))

        await db.commit()
