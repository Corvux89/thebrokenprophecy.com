

from flask import Blueprint, current_app, jsonify
from flask_discord import DiscordOAuth2Session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_

from constants import GUILD_ID, LIMIT
from models.entities import Adventure, Character


api_blueprint = Blueprint("api", __name__)

@api_blueprint.route('/adventures', methods=["GET"])
def adventures():
    discord_session: DiscordOAuth2Session = current_app.config.get('DISCORD_SESSION')
    db: SQLAlchemy = current_app.config.get('DB')

    db_adventures: list[Adventure] = db.session.query(Adventure).filter(and_(Adventure.guild_id == GUILD_ID, Adventure.end_ts == None))
    guild_members = discord_session.bot_request(f'/guilds/{GUILD_ID}/members?limit={LIMIT}', method='GET')
    characters = {c.player_id: c.name for c in db.session.query(Character).filter(Character.active == True, Character.guild_id == GUILD_ID).all()}

    data = []

    for a in db_adventures:
        players = [int(m['user']['id']) for m in guild_members if str(a.role_id) in m['roles']]

        a_dict = {"name": a.name,
                  "tier": a.tier,
                  "dms": [characters.get(p) for p in players if p in a.dms],
                  "players": [characters.get(p) for p in players if p not in a.dms]}
        
        data.append(a_dict)
        
    return jsonify(data)

