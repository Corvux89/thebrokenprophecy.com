import os

WEB_DEBUG = os.environ.get("DEBUG", False)

DB_URI = os.environ.get("DATABASE_URI", "")
SECRET_KEY = os.environ.get("SECRET_KEY", "")

COMMANDS_JSON = os.environ.get("COMMANDS_JSON", "")

GUILD_ID = os.environ.get("GUILD_ID", "")