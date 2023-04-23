from datetime import timedelta
from flask import Blueprint, session, current_app, redirect, url_for, request

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

@auth_blueprint.route('/')
def login():
    return current_app.discord.create_session(data=dict(redirect=request.args.get('next')))

@auth_blueprint.route('/logout')
def logout():
    current_app.discord.revoke()
    return redirect(url_for('homepage'))


