from functools import wraps
from flask import redirect, url_for, current_app, request
from flask_discord import DiscordOAuth2Session
from constants import ADMIN_ROLE, GUILD_ID, CHRON_ROLE


def is_admin(f):
    discord_session: DiscordOAuth2Session = current_app.config.get('DISCORD_SESSION')
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not discord_session.authorized:
            return redirect(url_for('auth.login', next=request.endpoint))

        user = discord_session.fetch_user()
        member = discord_session.bot_request(f'/guilds/{GUILD_ID}/members/{user.id}')

        if not has_role(member, ADMIN_ROLE):
            print(f'{user.name} tried to get access to admin menus')
            return redirect(url_for('homepage'))
        return f(*args, **kwargs)

    return decorated_function


def is_chronicler(f):
    discord_session: DiscordOAuth2Session = current_app.config.get('DISCORD_SESSION')
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not discord_session.authorized:
            return redirect(url_for('auth.login', next=request.endpoint))

        user = discord_session.fetch_user()
        member = discord_session.bot_request(f'/guilds/{GUILD_ID}/members/{user.id}')

        role_to_check = ADMIN_ROLE + CHRON_ROLE

        if not bool(set(role_to_check) & set(member['roles'])):
            return redirect(url_for('homepage'))
        return f(*args, **kwargs)

    return decorated_function


def has_role(member, roles_to_check):
    return True if len([r for r in member['roles'] if r in roles_to_check]) > 0 else False
