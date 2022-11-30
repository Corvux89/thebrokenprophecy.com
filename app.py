import json

import flask
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_talisman import Talisman
from flask_sqlalchemy import SQLAlchemy

from constants import WEB_DEBUG, DB_URI, SECRET_KEY
from helpers.helpers import get_race_data, get_class_data

app = Flask(__name__)

db = SQLAlchemy()

app.config["SQLALCHEMY_DATABASE_URI"] = DB_URI
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
app.secret_key = SECRET_KEY

app.config.update(
    DEBUG=WEB_DEBUG
)


@app.route('/')
@app.route('/home')
def homepage():
    return render_template("main.html")

@app.route('/server_stats')
def census():
    # race_fig = get_race_data(db.session)
    # class_fig = get_class_data(db.session)
    # return render_template('census.html', race_graph=race_fig, class_graph=class_fig)
    return flask.redirect('/')

@app.route('/commands')
def bot():
    f = open('static/commands.json')
    commands = json.load(f)

    return render_template('commands.html', commands=commands['category'])



csp = {
    'default-src': [
        '\'self\'',
        'https://docs.google.com',
        'https://code.jquery.com/'
        'https://cdn.jsdelivr.net/npm/',
        'https://www.googletagmanager.com/',
        'https://analytics.google.com/',
        'https://www.google-analytics.com/'
    ],
    'script-src': [
        '\'self\'',
        '\'unsafe-eval\'',
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
        '\'unsafe-inline\'',
        'https://cdn.jsdelivr.net/',
        'https://cdn.plot.ly/'
        'plotly.js'
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

# db.init_app(app)

if __name__ == "__main__":
    app.run()
