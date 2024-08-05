from urllib.parse import urlparse

from flask import Flask, render_template, make_response, request
from flask_bootstrap import Bootstrap
from flask_talisman import Talisman
from flask_discord import DiscordOAuth2Session

from blueprints.admin.admin import admin_blueprint
from blueprints.adventures import adventures_blueprint
from blueprints.auth import auth_blueprint
from blueprints.chronicle import chronicle_blueprint
from blueprints.commands import commands_blueprint
from blueprints.factions import factions_blueprint
from blueprints.characters import characters_blueprint
from blueprints.stats import stats_blueprint
from blueprints.api import api_blueprint

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
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "true"  # DEV ONLY!!!!


app.config['DISCORD_SESSION'] = DiscordOAuth2Session(app)
app.config['DB'] = db =  SQLAlchemy()
db.init_app(app)


@app.errorhandler(404)
def not_found(e):
    return render_template('404.html')

@app.route('/')
@app.route('/home')
def homepage():
    return render_template("main.html")

@app.route('/sitemap.xml')
def site_map():
    host_components = urlparse(request.host_url)
    host_base = host_components.scheme + "://" + host_components.netloc
    static_urls = []

    for rule in app.url_map.iter_rules():
        if not str(rule).startswith("/admin") and not str(rule).startswith("/user") and not str(rule).startswith("/chromatic_chronicle/editor"):
            if "GET" in rule.methods and len(rule.arguments) == 0:
                url = {"loc": f"{host_base}{str(rule)}"}
                static_urls.append(url)
    response = render_template('sitemap.xml', static_urls=static_urls, host_base=host_base)
    response = make_response(response)
    response.headers["Content-Type"] = "application/xml"
    return response


csp = get_csp()

Bootstrap(app)
talisman = Talisman(
    app,
    content_security_policy=csp,
    content_security_policy_nonce_in=['script-src', 'script-src-elem', 'style-src']
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
app.register_blueprint(api_blueprint, url_prefix='/api')

if __name__ == "__main__":
    app.run()
