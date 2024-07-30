import traceback

from flask import Blueprint, current_app, redirect, url_for, request, session
from flask_discord import DiscordOAuth2Session

from helpers import is_chronicler, is_admin

auth_blueprint = Blueprint("auth", __name__)

def redirect_dest(fallback):
    dest = request.args.get('next')
    return redirect(url_for(dest)) if dest else redirect(fallback)

@auth_blueprint.route('/')
def login():
    discord_session: DiscordOAuth2Session = current_app.config.get('DISCORD_SESSION')
    if discord_session:
        return current_app.discord.create_session(data={'redirect': request.args.get('next', 'homepage')})
    return redirect(url_for('homepage'))

@auth_blueprint.route('/logout')
def logout():
    discord_session: DiscordOAuth2Session = current_app.config.get('DISCORD_SESSION')
    discord_session.revoke()
    session.pop("Council") if session.get("Council") else ''
    session.pop("Chronicler") if session.get("Chronicler") else ''
    return redirect(url_for('homepage'))

@auth_blueprint.route('/callback')
def callback():
    redirect_to = None
    try:
        data = current_app.discord.callback()
        redirect_to = data.get("redirect", "/")
    except Exception as e:
        print(f"Issue with callback: {e}\n{traceback.print_exc()}")
        print(f'{current_app.discord.client_id} | {current_app.discord.user_id}')
        pass

    if is_admin:
        session["Council"] = True

    if is_chronicler:
        session["Chronicler"] = True

    if not redirect_to:
        redirect_to = 'homepage'
    return redirect(url_for(redirect_to))