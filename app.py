import traceback

from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_talisman import Talisman
from flask_discord import DiscordOAuth2Session
from werkzeug.security import generate_password_hash

from blueprints.admin import admin_blueprint
from blueprints.adventures import adventures_blueprint
from blueprints.auth import auth_blueprint
from blueprints.chronicle import chronicle_blueprint
from blueprints.commands import commands_blueprint
from blueprints.factions import factions_blueprint
from blueprints.characters import characters_blueprint
from blueprints.stats import stats_blueprint

from constants import *
from helpers import get_csp
from models import *

app = Flask(__name__)

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

if WEB_DEBUG:
    print("Debugging!")
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "true" # DEV ONLY!!!!

app.db = db = SQLAlchemy()
app.discord = discord = DiscordOAuth2Session(app)

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html')

@app.route("/callback/")
def callback():
    redirect_to = None
    try:
        data = discord.callback()
        redirect_to = data.get("redirect", "/")
    except Exception as e:
        print(f"Issue with callback: {e}\n{traceback.print_exc()}")
        print(f'{discord.client_id} | {discord.user_id} | {discord.get_authorization_token()} | {discord.fetch_connections()} ')
        pass
    if not redirect_to:
        redirect_to = 'homepage'
    return redirect(url_for(redirect_to))

@app.route('/')
@app.route('/home')
def homepage():
    return render_template("main.html")


@app.route('/credits')
def credits():
    return render_template('credits.html')

@app.route('/password/<password>')
def password(password):
    return f'<p>{generate_password_hash(password)}</p>'


csp = get_csp()

Bootstrap(app)
talisman = Talisman(
    app,
    content_security_policy=csp,
    content_security_policy_nonce_in=['script-src', 'script-src-elem']
)

# Blueprints
app.register_blueprint(auth_blueprint, url_prefix='/login')
app.register_blueprint(admin_blueprint, url_prefix='/admin')
app.register_blueprint(commands_blueprint, url_prefix='/commands')
app.register_blueprint(stats_blueprint, url_prefix="/server_stats")
app.register_blueprint(factions_blueprint, url_prefix="/factions")
app.register_blueprint(adventures_blueprint, url_prefix="/adventures")
app.register_blueprint(chronicle_blueprint, url_prefix="/chromatic_chronicle")
app.register_blueprint(characters_blueprint, url_prefix='/characters')

db.init_app(app)

if __name__ == "__main__":
    app.run()
