import os

WEB_DEBUG = os.environ.get("DEBUG", False)

DB_URI = os.environ.get("DATABASE_URI", "")
SECRET_KEY = os.environ.get("SECRET_KEY", "")

GUILD_ID = os.environ.get("GUILD_ID", "")

USERNAME = os.environ.get("USERNAME", "admin")
PASSWORD = os.environ.get("PASSWORD", "password")