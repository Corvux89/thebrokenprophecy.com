import json

import flask
import flask_login
from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_talisman import Talisman
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user

from constants import WEB_DEBUG, DB_URI, SECRET_KEY, USERNAME, PASSWORD
from helpers.helpers import get_race_table, get_class_table
from models.user import User

app = Flask(__name__)

db = SQLAlchemy()

login_manager = LoginManager()

app.config["SQLALCHEMY_DATABASE_URI"] = DB_URI
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
app.secret_key = SECRET_KEY

app.config.update(
    DEBUG=WEB_DEBUG
)

admin_user = {USERNAME: {"pw": PASSWORD}}


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


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if flask.request.method == 'POST':
        username = flask.request.form.get('username')
        if flask.request.form.get('pw') == admin_user[username]['pw']:
            user = User()
            user.id = username
            flask_login.login_user(user)
            return redirect(url_for('admin_menu'))
    elif current_user.is_authenticated:
        return redirect(url_for('admin_menu'))
    else:
        return render_template("login.html")

    return render_template('main.html')

@app.route('/admin_menu')
@flask_login.login_required
def admin_menu():
    return render_template('/admin_pages/admin_menu.html')


@app.route('/')
@app.route('/home')
def homepage():
    return render_template("main.html")


@app.route('/credits')
def credits():
    return render_template('credits.html')


@app.route('/server_stats')
def census():
    race_data = get_race_table(db.session)
    class_data = get_class_table(db.session)

    return render_template('server_stats.html', race_data=race_data, class_data=class_data)


@app.route('/commands')
def bot():
    f = open('static/commands.json')
    commands = json.load(f)
    return render_template('commands.html', commands=commands['category'])

@app.route('/factions')
def faction_list():
    f = open('static/factions.json')
    guild = json.load(f)
    return render_template('faction_list.html', guild=guild)

@app.route('/factions/<faction>')
def faction(faction):
    f = open('static/factions.json')
    guild = json.load(f)
    for f in guild['faction']:
        if f['key'] == faction:
            faction_info = f
            break
    return render_template('faction.html', faction=faction_info)




csp = {
    'default-src': [
        '\'self\'',
        'https://docs.google.com',
        'https://code.jquery.com/'
        'https://cdn.jsdelivr.net/npm/',
        'https://www.googletagmanager.com/',
        'https://analytics.google.com/',
        'https://www.google-analytics.com/',
        'https://use.fontawesome.com'
    ],
    'script-src': [
        '\'self\'',
        'https://cdn.jsdelivr.net/',
        'https://www.googletagmanager.com/',
        'https://ajax.googleapis.com',
        'https://cdn.plot.ly/plotly-latest.min.js',
        'https://cdnjs.cloudflare.com/'
        'plotly.js'
    ],
    'img-src': [
        '*',
        'data:'
    ],
    'style-src': [
        '\'self\'',
        'https://cdn.jsdelivr.net/',
        'https://cdn.plot.ly/'
        'plotly.js',
        'https://use.fontawesome.com'
    ],
    'script-src-elem': [
        '\'self\'',
        'https://cdnjs.cloudflare.com/',
        'https://cdn.jsdelivr.net/',
        'https://cdn.plot.ly',
        'https://ajax.googleapis.com'
    ]
}

Bootstrap(app)
talisman = Talisman(
    app,
    content_security_policy=csp,
    content_security_policy_nonce_in=['script-src', 'script-src-elem']
)

db.init_app(app)
login_manager.init_app(app)

if __name__ == "__main__":
    app.run()
