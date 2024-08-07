

import math
from flask import Blueprint, abort, current_app, jsonify, request, session
from flask_discord import DiscordOAuth2Session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Boolean, Integer, String, and_, cast, literal, union, select
from sqlalchemy.dialects.postgresql import ARRAY

from constants import GUILD_ID, LIMIT
from helpers.auth_helpers import requires_auth
from models.categories import BlackSmithType, CharacterClass, CharacterRace, CharacterSubclass, CharacterSubrace, ConsumableType, MagicSchool, Rarity
from models.entities import Adventure, BlackSmithItem, Character, ConsumableItem, PlayerCharacterClass, ScrollItem, WondrousItem


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

@api_blueprint.route('/characters', methods=["GET"])
def characters():
    db: SQLAlchemy = current_app.config.get('DB')

    characters = db.session.query(
        Character.id,
        Character.name,
        Character.player_id,
        CharacterRace.id.label("race_id"),
        CharacterRace.value.label("race"),
        CharacterSubrace.id.label("subrace_id"),
        CharacterSubrace.value.label("subrace"),
        Character.xp
    ).outerjoin(CharacterSubrace, CharacterSubrace.id == Character.subrace)\
     .join(CharacterRace, CharacterRace.id == Character.race)\
     .filter(and_(Character.active == True, Character.guild_id == GUILD_ID)).all()
    
    character_classes = db.session.query(
        PlayerCharacterClass.character_id,
        CharacterClass.id.label("primary_class_id"),
        CharacterClass.value.label("primary_class"),
        CharacterSubclass.id.label("subclass_id"),
        CharacterSubclass.value.label("subclass")
    ).outerjoin(CharacterSubclass, CharacterSubclass.id == PlayerCharacterClass.subclass)\
     .join(CharacterClass, CharacterClass.id == PlayerCharacterClass.primary_class)\
     .filter(and_(PlayerCharacterClass.character_id.in_([c.id for c in characters]), PlayerCharacterClass.active == True)).all()
    
    data = []
    
    for char in characters:
        c_dict = {
            "name": char.name,
            "race": {"id": char.race_id, "value": char.race},
            "subrace": {"id": char.subrace_id, "value": char.subrace} if char.subrace_id else '',
            "classes": [{
                "id": c.primary_class_id,
                "value": c.primary_class,
                "subclasses": [
                    {
                        "id": c.subclass_id,
                        "value": c.subclass
                    }
                ] if c.subclass_id else []
            } for c in character_classes if c.character_id == char.id and c.primary_class is not None]
        }

        if session.get("Council"):
            c_dict["level"] = math.ceil((char.xp +1)/1000)

        data.append(c_dict)

    return jsonify(data)

@api_blueprint.route('/races', methods=["GET"])
def races():
    db: SQLAlchemy = current_app.config.get('DB')

    races = db.session.query(CharacterRace).all()
    subraces = db.session.query(CharacterSubrace).all()

    data = [{"id": r.id, 
             "value": r.value, 
             "subraces": [{
                 "id": s.id,
                 "value": s.value
             } for s in subraces if s.parent == r.id]} for r in races]

    return jsonify(data)

@api_blueprint.route('/classes', methods=["GET"])
def classes():
    db: SQLAlchemy = current_app.config.get('DB')

    classes = db.session.query(CharacterClass).all()
    subclasses = db.session.query(CharacterSubclass).all()

    data = [{"id": c.id, 
             "value": c.value,
             "subclasses": [{
                 "id": s.id,
                 "value": s.value
             } for s in subclasses if s.parent == c.id]} for c in classes]

    return jsonify(data)

@api_blueprint.route('/items', methods=["GET", "PATCH"])
@api_blueprint.route('/items/<table>/<item>', methods=["GET"])
@requires_auth
def items(table: str = None, item: int = None):
    db: SQLAlchemy = current_app.config.get('DB')

    if request.method == "PATCH":
        obj = request.get_json()

        return "cool"

    queries = []
    classes = []

    if table is None or table == "Blacksmith":
        s1 = select(BlackSmithItem.id,
                    BlackSmithItem.name,
                    BlackSmithItem.cost,
                    BlackSmithItem.item_modifier,
                    BlackSmithItem.attunement,
                    BlackSmithItem.source,
                    cast(literal(None), Integer).label('level'),
                    cast(literal(None), ARRAY(Integer)).label('classes'),
                    cast(literal(None), Integer).label('school_id'),
                    cast(literal(None), String).label('school'),
                    BlackSmithType.id.label("type_id"),
                    BlackSmithType.value.label('type'),
                    BlackSmithItem.seeking_only,
                    Rarity.id.label("rarity_id"),
                    Rarity.value.label('rarity'),
                    BlackSmithItem.notes,
                    literal('Blacksmith').label('table')) \
            .join(BlackSmithType, BlackSmithItem.sub_type == BlackSmithType.id) \
            .join(Rarity, BlackSmithItem.rarity == Rarity.id)
        if item:
            s1 = s1.where(BlackSmithItem.id == item)
        queries.append(s1)

    if table is None or table == "Consumable":
        s2 = select(ConsumableItem.id,
                    ConsumableItem.name,
                    ConsumableItem.cost,
                    cast(literal(None),Boolean).label('item_modifier'),
                    ConsumableItem.attunement,
                    ConsumableItem.source,
                    cast(literal(None), Integer).label('level'),
                    cast(literal(None), ARRAY(Integer)).label('classes'),
                    cast(literal(None), Integer).label('school_id'),
                    cast(literal(None), String).label('school'),
                    ConsumableType.id.label("type_id"),
                    ConsumableType.value.label('type'),
                    cast(literal(None), Boolean).label("seeking_only"),
                    Rarity.id.label("rarity_id"),
                    Rarity.value.label('rarity'),
                    ConsumableItem.notes,
                    literal('Consumable').label('table')) \
            .join(ConsumableType, ConsumableItem.sub_type == ConsumableType.id) \
            .join(Rarity, ConsumableItem.rarity == Rarity.id)
        if item:
            s2 = s2.where(ConsumableItem.id == item)
        queries.append(s2)

    if table is None or table == "Scroll":
        classes = db.session.query(CharacterClass).all()
        s3 = select(ScrollItem.id,
                    ScrollItem.name,
                    ScrollItem.cost,
                    cast(literal(None),Boolean).label('item_modifier'),
                    cast(literal(None), Boolean).label('attunement'),
                    ScrollItem.source,
                    ScrollItem.level,
                    ScrollItem.classes,
                    MagicSchool.id.label('school_id'),
                    MagicSchool.value.label('school'),
                    cast(literal(None), Integer).label('type_id'),
                    cast(literal(None), String).label('type'),
                    cast(literal(None), Boolean).label("seeking_only"),
                    Rarity.id.label("rarity_id"),
                    Rarity.value.label('rarity'),
                    ScrollItem.notes,
                    literal('Scroll').label('table')) \
            .join(MagicSchool, ScrollItem.school == MagicSchool.id)\
            .join(Rarity, ScrollItem.rarity == Rarity.id)
        if item:
            s3 = s3.where(ScrollItem.id == item)
        queries.append(s3)

    if table is None or table == "Wondrous":
        s4 = select(WondrousItem.id,
                    WondrousItem.name,
                    WondrousItem.cost,
                    cast(literal(None),Boolean).label('item_modifier'),
                    WondrousItem.attunement,
                    WondrousItem.source,
                    cast(literal(None), Integer).label('level'),
                    cast(literal(None), ARRAY(Integer)).label('classes'),
                    cast(literal(None), Integer).label('school_id'),
                    cast(literal(None), String).label('school'),
                    cast(literal(None), Integer).label('type_id'),
                    cast(literal(None), String).label('type'),
                    WondrousItem.seeking_only,
                    Rarity.id.label("rarity_id"),
                    Rarity.value.label('rarity'),
                    WondrousItem.notes,
                    literal('Wondrous').label('table')) \
            .join(Rarity, WondrousItem.rarity == Rarity.id)
        if item:
            s4 = s4.where(WondrousItem.id == item)
        queries.append(s4)

    u = union(*queries).alias('items')

    vals = db.session.query(u).all()

    data = [{"name": v.name, 
             "id": v.id, 
             "cost": v.cost, 
             "type": {"id": v.type_id,"value": v.type} if v.type_id else {}, 
             "rarity": {"id": v.rarity_id, "value": v.rarity}, 
             "attunement": v.attunement or "",
             "item_modifier": v.item_modifier or "",
             "seeking_only": v.seeking_only or "",
             "source": v.source,
             "school": {"id": v.school_id, "value": v.school} if v.school_id else {},
             "classes": [{"id": c.id, "value": c.value} for c in classes if c.id in v.classes] if v.classes else [],
             "level": v.level or "",
             "notes": v.notes,
             "table": v.table} 
             for v in vals]

    return jsonify(data if len(data) > 1 else data[0])

@api_blueprint.route('/rarity', methods=['GET'])
@requires_auth
def rarity():
    db: SQLAlchemy = current_app.config.get('DB')
    rarity = db.session.query(Rarity).all()
    data = [{"id": r.id, "value": r.value} for r in rarity]
    return jsonify(data)

@api_blueprint.route('/item_type/<table>', methods=['GET'])
def item_type(table: str = None):
    db: SQLAlchemy = current_app.config.get('DB')

    table_map = {
        "Blacksmith": BlackSmithType,
        "Consumable": ConsumableType,
    }

    if not table_map.get(table):
        abort(400)

    type = db.session.query(table_map.get(table))

    data = [{"id": t.id, "value": t.value} for t in type]

    return jsonify(data)

@api_blueprint.route('/magic_schools', methods=['GET'])
@requires_auth
def magic_schools():
    db: SQLAlchemy = current_app.config.get('DB')
    schools = db.session.query(MagicSchool).all()
    data = [{"id": s.id, "value": s.value} for s in schools]
    return jsonify(data)