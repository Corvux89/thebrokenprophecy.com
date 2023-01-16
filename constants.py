import os

WEB_DEBUG = os.environ.get("DEBUG", False)

DB_URI = os.environ.get("DATABASE_URI", "")
SECRET_KEY = os.environ.get("SECRET_KEY", "")

GUILD_ID = os.environ.get("GUILD_ID", "")

USERNAME = os.environ.get("USERNAME", "admin")
PASSWORD = os.environ.get("PASSWORD", "password")

DISCORD_CLIENT_ID = os.environ.get("DISCORD_CLIENT_ID", "")
DISCORD_CLIENT_SECRET = os.environ.get("DISCORD_CLIeNT_SECRET", "")
DISCORD_BOT_TOKEN = os.environ.get("DISCORD_BOT_TOKEN", "")
OAUTH_REDIRECT_URI = os.environ.get("OAUTH_REDIRECT_URI", "")
OAUTH_SCOPE = os.environ.get("OAUTH_SCOPE", "")
LIMIT = os.environ.get("LIMIT", 1)


admin_user = {USERNAME: {"pw": PASSWORD}}

