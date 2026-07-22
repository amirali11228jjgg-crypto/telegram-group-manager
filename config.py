import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

DATABASE_NAME = "database.db"

MAX_WARNS = 3

MUTE_TIME = 3600

LINK_FILTER = True

AUTO_BAN = True
