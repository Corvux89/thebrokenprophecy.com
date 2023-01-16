from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_talisman import Talisman
from flask_login import LoginManager
from flask_discord import DiscordOAuth2Session
from blueprints.admin import admin_blueprint
from blueprints.adventures import adventures_blueprint
from blueprints.commands import commands_blueprint
from blueprints.factions import factions_blueprint
from blueprints.stats import stats_blueprint

from constants import *
from helpers import get_csp
from models import *

app = Flask(__name__)

login_manager = LoginManager()

app.config["SQLALCHEMY_DATABASE_URI"] = DB_URI
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
app.config["DISCORD_CLIENT_ID"] = DISCORD_CLIENT_ID
app.config["DISCORD_REDIRECT_URI"] = OAUTH_REDIRECT_URI
app.config["DISCORD_BOT_TOKEN"] = DISCORD_BOT_TOKEN
app.config["DISCORD_CLIENT_SECRET"] = DISCORD_CLIENT_SECRET
app.secret_key = SECRET_KEY

app.config.update(
    DEBUG=WEB_DEBUG
)

app.db = db = SQLAlchemy()
app.discord = discord = DiscordOAuth2Session(app)


@login_manager.user_loader
def user_loader(username):
    if username not in admin_user:
        return

    user = User()
    user.id = username
    return user


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    if not username or username not in admin_user:
        return
    user = User()
    user.id = username
    return user


@app.route('/')
@app.route('/home')
def homepage():
    return render_template("main.html")


@app.route('/credits')
def credits():
    return render_template('credits.html')


csp = get_csp()

Bootstrap(app)
talisman = Talisman(
    app,
    content_security_policy=csp,
    content_security_policy_nonce_in=['script-src', 'script-src-elem']
)

# Blueprints
app.register_blueprint(admin_blueprint, url_prefix='/admin')
app.register_blueprint(commands_blueprint, url_prefix='/commands')
app.register_blueprint(stats_blueprint, url_prefix="/server_stats")
app.register_blueprint(factions_blueprint, url_prefix="/factions")
app.register_blueprint(adventures_blueprint, url_prefix="/adventures")

db.init_app(app)
login_manager.init_app(app)

if __name__ == "__main__":
    app.run()
