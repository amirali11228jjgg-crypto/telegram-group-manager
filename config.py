import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")

print("TOKEN CHECK:", BOT_TOKEN[:10] if BOT_TOKEN else "EMPTY")
