import sqlite3

DB_NAME = "bot.db"


def connect():
    return sqlite3.connect(DB_NAME)


def create_tables():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS settings (
        chat_id INTEGER PRIMARY KEY,
        anti_link INTEGER DEFAULT 1,
        welcome INTEGER DEFAULT 1
    )
    """)

    conn.commit()
    conn.close()


def get_settings(chat_id):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM settings WHERE chat_id=?",
        (chat_id,)
    )

    result = cur.fetchone()

    if not result:
        cur.execute(
            "INSERT INTO settings(chat_id) VALUES(?)",
            (chat_id,)
        )
        conn.commit()
        result = (chat_id, 1, 1)

    conn.close()
    return result
