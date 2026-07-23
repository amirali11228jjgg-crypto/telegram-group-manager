import aiosqlite

DB_NAME = "bot.db"


async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:

        await db.execute("""
        CREATE TABLE IF NOT EXISTS warnings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            username TEXT,
            reason TEXT,
            admin_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        await db.commit()


async def add_warning(user_id, username, reason, admin_id):
    async with aiosqlite.connect(DB_NAME) as db:

        await db.execute(
            """
            INSERT INTO warnings
            (user_id, username, reason, admin_id)
            VALUES (?, ?, ?, ?)
            """,
            (
                user_id,
                username,
                reason,
                admin_id
            )
        )

        await db.commit()


async def get_warnings(user_id):
    async with aiosqlite.connect(DB_NAME) as db:

        cursor = await db.execute(
            """
            SELECT reason, created_at
            FROM warnings
            WHERE user_id = ?
            ORDER BY id DESC
            """,
            (user_id,)
        )

        return await cursor.fetchall()


async def clear_warnings(user_id):
    async with aiosqlite.connect(DB_NAME) as db:

        await db.execute(
            """
            DELETE FROM warnings
            WHERE user_id = ?
            """,
            (user_id,)
        )

        await db.commit()
