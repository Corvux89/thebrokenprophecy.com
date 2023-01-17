from datetime import timedelta

import flask
from flask import Blueprint, session, current_app, redirect, url_for, render_template, request, flash
from flask_login import login_user, current_user
from sqlalchemy import and_
from werkzeug.security import check_password_hash

from models import User

auth_blueprint = Blueprint("auth", __name__)

def redirect_dest(fallback):
    dest = request.args.get('next')
    try:
        dest_url = url_for(dest)
    except:
        return redirect(fallback)
    return redirect(dest_url)

@auth_blueprint.before_request
def make_session_permanent():
    session.permanent = True
    current_app.permanent_session_lifetime = timedelta(minutes=30)

@auth_blueprint.route('/', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'POST':
        if flask.request.method == 'POST':
            username = flask.request.form.get('username')
            password = flask.request.form.get('pw')

            user = current_app.db.session.query(User).filter(and_(User.username == username, User.active == True)).first()

            if not user or not check_password_hash(user.password, password):
                flash('Invalid username/login')
                return redirect_dest(url_for('homepage'))

            login_user(user, remember=True)
            session['user_id'] = user.id
            return redirect_dest(url_for('homepage'))
    elif current_user.is_authenticated:
        return redirect_dest(url_for('homepage'))
    else:
        return render_template("login.html", url=redirect_dest('homepage'))

