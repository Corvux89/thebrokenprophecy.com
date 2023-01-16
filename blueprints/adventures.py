from flask import Blueprint, current_app, url_for, redirect, render_template

from constants import GUILD_ID, LIMIT
from helpers import get_adventures

adventures_blueprint = Blueprint("adventures", __name__)

@adventures_blueprint.route('/')
def adventure_list():
    guild_members = current_app.discord.bot_request(f'/guilds/{GUILD_ID}/members?limit={LIMIT}', method='GET')
    adventures = get_adventures(guild_members)


    return render_template('adventures.html', adventures=adventures)