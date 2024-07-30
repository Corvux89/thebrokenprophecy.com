from flask import Blueprint, current_app, url_for, redirect, render_template
from flask_discord import DiscordOAuth2Session

from constants import GUILD_ID, LIMIT
from helpers import get_adventures

adventures_blueprint = Blueprint("adventures", __name__)


@adventures_blueprint.route('/')
def adventure_list():
    discord_session: DiscordOAuth2Session = current_app.config.get('DISCORD_SESSION')
    guild_members = discord_session.bot_request(f'/guilds/{GUILD_ID}/members?limit={LIMIT}', method='GET')
    adventures = get_adventures(guild_members)

    return render_template('/adventures/adventures.html', adventures=adventures)
