import json
import os

WEB_DEBUG = os.environ.get("DEBUG", False)

DB_URI = os.environ.get("DATABASE_URI", "")
SECRET_KEY = os.environ.get("SECRET_KEY", "")

GUILD_ID = os.environ.get("GUILD_ID", "")

DISCORD_CLIENT_ID = os.environ.get(r"DISCORD_CLIENT_ID", "")
DISCORD_CLIENT_SECRET = os.environ.get("DISCORD_CLIENT_SECRET", "")
DISCORD_BOT_TOKEN = os.environ.get("DISCORD_BOT_TOKEN", "")
OAUTH_REDIRECT_URI = os.environ.get("OAUTH_REDIRECT_URI", "")
LIMIT = os.environ.get("LIMIT", 1)


# Admin User
ADMIN_ROLE = json.loads(os.environ["ADMIN_ROLES"]) if "ADMIN_ROLES" in os.environ else []

# Chronicler
CHRON_ROLE = json.loads(os.environ["CHRON_ROLES"]) if "CHRON_ROLES" in os.environ else []


