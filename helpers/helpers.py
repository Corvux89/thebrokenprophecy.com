import math
from sqlalchemy import and_, func

from constants import GUILD_ID
from models import *
from flask import current_app


def get_race_table():
    db: SQLAlchemy = current_app.config.get('DB')
    races = db.session.query(CharacterRace).all()
    race_count = db.session.query(CharacterRace.value, func.count(Character.race).label("count")) \
        .filter(and_(Character.active == True, Character.guild_id == GUILD_ID)) \
        .join(CharacterRace, Character.race == CharacterRace.id) \
        .group_by(CharacterRace.value).all()

    total_count = db.session.query(Character).filter(
        and_(Character.active == True, Character.guild_id == GUILD_ID)).count()

    stat = dict()
    stat['total'] = total_count
    stat['races'] = []

    for r in races:
        race_dict = {"name": r.value, "count": 0, "subraces": []}
        for c in race_count:
            if c.value == r.value:
                race_dict["count"] = c.count
                break
        stat['races'].append(race_dict)

    subraces = db.session.query(CharacterSubrace) \
        .join(CharacterRace, CharacterRace.id == CharacterSubrace.parent) \
        .add_columns(CharacterSubrace.id, CharacterSubrace.value, CharacterRace.value.label("race")).all()

    subrace_count = db.session.query(CharacterSubrace.id, func.count(Character.subrace).label("count")) \
        .filter(and_(Character.active == True, Character.guild_id == GUILD_ID)) \
        .join(CharacterSubrace, Character.subrace == CharacterSubrace.id) \
        .group_by(CharacterSubrace.id).all()

    for s in subraces:
        sub_dict = {"name": s.value, "count": 0}
        for c in subrace_count:
            if c.id == s.id:
                sub_dict["count"] = c.count
                break

        for r in stat['races']:
            if r['name'] == s.race:
                r["subraces"].append(sub_dict)
                break

    stat["races"] = sorted(stat["races"], key=lambda r: r["name"])

    return stat


def get_class_table():
    db: SQLAlchemy = current_app.config.get('DB')
    classes = db.session.query(CharacterClass).all()
    class_count = db.session.query(CharacterClass.value, func.count(PlayerCharacterClass.primary_class).label("count")) \
        .filter(and_(Character.active == True, Character.guild_id == GUILD_ID, PlayerCharacterClass.active == True)) \
        .join(CharacterClass, PlayerCharacterClass.primary_class == CharacterClass.id) \
        .join(Character, PlayerCharacterClass.character_id == Character.id) \
        .group_by(CharacterClass.value).all()

    stat = dict()
    stat['classes'] = []

    for c in classes:
        class_dict = {"name": c.value, "count": 0, "subclasses": []}
        for i in class_count:
            if i.value == c.value:
                class_dict["count"] = i.count
                break
        stat["classes"].append(class_dict)

    subclasses = db.session.query(CharacterSubclass) \
        .join(CharacterClass, CharacterClass.id == CharacterSubclass.parent) \
        .add_columns(CharacterSubclass.id, CharacterSubclass.value, CharacterClass.value.label("char_class")).all()

    subclass_count = db.session.query(CharacterSubclass.id, func.count(PlayerCharacterClass.subclass).label("count")) \
        .filter(and_(Character.active == True, Character.guild_id == GUILD_ID, PlayerCharacterClass.active == True)) \
        .join(CharacterSubclass, PlayerCharacterClass.subclass == CharacterSubclass.id) \
        .join(Character, PlayerCharacterClass.character_id == Character.id) \
        .group_by(CharacterSubclass.id).all()

    for s in subclasses:
        sub_dict = {"name": s.value, "count": 0}
        for c in subclass_count:
            if c.id == s.id:
                sub_dict["count"] = c.count
                break

        for r in stat["classes"]:
            if r["name"] == s.char_class:
                r["subclasses"].append(sub_dict)
                break

    player_count = db.session.query(PlayerCharacterClass.character_id,
                                 func.count(PlayerCharacterClass.character_id).label("count")) \
        .filter(and_(Character.active == True, Character.guild_id == GUILD_ID,
                     PlayerCharacterClass.active == True)) \
        .join(Character, PlayerCharacterClass.character_id == Character.id) \
        .group_by(PlayerCharacterClass.character_id).all()

    stat["classes"] = sorted(stat["classes"], key=lambda c: c["name"])

    m_dict = {"name": "Multiclass", "subclasses": []}
    m_count = 0
    for p in player_count:
        if p.count > 1:
            m_count += 1
    m_dict["count"] = m_count

    stat["classes"].append(m_dict)

    return stat

def get_characters():
    db: SQLAlchemy = current_app.config.get('DB')
    characters = db.session.query(Character)\
        .outerjoin(CharacterSubrace, CharacterSubrace.id == Character.subrace)\
        .join(CharacterRace, CharacterRace.id == Character.race)\
        .filter(and_(Character.active == True, Character.guild_id == GUILD_ID))\
        .add_columns(Character.id, Character.name, Character.player_id, CharacterRace.value.label("race"), CharacterSubrace.value.label("subrace"), Character.xp).all()

    d_out = []

    for c in characters:
        c_dict = {"name": c.name, "race": c.race, "subrace": c.subrace, "classes": [], "level": math.ceil((c.xp +1)/1000)}

        char_class = db.session.query(PlayerCharacterClass)\
            .join(CharacterClass, CharacterClass.id == PlayerCharacterClass.primary_class)\
            .outerjoin(CharacterSubclass, CharacterSubclass.id == PlayerCharacterClass.subclass)\
            .filter(and_(PlayerCharacterClass.character_id == c.id, PlayerCharacterClass.active == True))\
            .add_columns(CharacterClass.value.label("Class"), CharacterSubclass.value.label("Subclass")).all()

        for cl in char_class:
            c_dict["classes"].append({"prim_class": cl.Class, "subclass": cl.Subclass})

        c_dict["primary_class"] = "<br>".join(f'{x["prim_class"]}' for x in c_dict["classes"])
        c_dict["subclasses"] = "<br>".join(f'{x["subclass"]}' for x in c_dict["classes"])

        d_out.append(c_dict)


    return d_out

