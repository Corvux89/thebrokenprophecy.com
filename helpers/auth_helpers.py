from functools import wraps
from flask import redirect, url_for, current_app, request, session
from constants import ADMIN_ROLE, GUILD_ID, CHRON_ROLE


def is_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_app.discord.authorized:
            return redirect(url_for('auth.login', next=request.endpoint))

        user = current_app.discord.fetch_user()
        member = current_app.discord.bot_request(f'/guilds/{GUILD_ID}/members/{user.id}')

        if not has_role(member, ADMIN_ROLE):
            print(f'{user.name} tried to get access to admin menus')
            return redirect(url_for('homepage'))
        return f(*args, **kwargs)

    return decorated_function


def is_chronicler(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_app.discord.authorized:
            return redirect(url_for('auth.login', next=request.endpoint))

        user = current_app.discord.fetch_user()
        member = current_app.discord.bot_request(f'/guilds/{GUILD_ID}/members/{user.id}')

        role_to_check = ADMIN_ROLE + CHRON_ROLE

        s = session

        if not bool(set(role_to_check) & set(member['roles'])):
            return redirect(url_for('homepage'))
        return f(*args, **kwargs)

    return decorated_function


def has_role(member, roles_to_check):
    return True if len([r for r in member['roles'] if r in roles_to_check]) > 0 else False
