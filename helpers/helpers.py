from sqlalchemy import and_, func

from constants import GUILD_ID
from models import *


def get_race_table(session):
    races = session.query(CharacterRace).all()
    race_count = session.query(CharacterRace.value, func.count(Character.race).label("count")) \
        .filter(and_(Character.active == True, Character.guild_id == GUILD_ID)) \
        .join(CharacterRace, Character.race == CharacterRace.id) \
        .group_by(CharacterRace.value).all()

    total_count = session.query(Character).filter(
        and_(Character.active == True, Character.guild_id == GUILD_ID)).count()

    stat = dict()
    stat['total'] = total_count
    stat['races'] = []

    for r in races:
        race_dict = {}
        race_dict["name"] = r.value
        race_dict["count"] = 0
        race_dict["subraces"] = []
        for c in race_count:
            if c.value == r.value:
                race_dict["count"] = c.count
                break
        stat['races'].append(race_dict)

    subraces = session.query(CharacterSubrace) \
        .join(CharacterRace, CharacterRace.id == CharacterSubrace.parent) \
        .add_columns(CharacterSubrace.id, CharacterSubrace.value, CharacterRace.value.label("race")).all()

    subrace_count = session.query(CharacterSubrace.value, func.count(Character.subrace).label("count")) \
        .filter(and_(Character.active == True, Character.guild_id == GUILD_ID)) \
        .join(CharacterSubrace, Character.subrace == CharacterSubrace.id) \
        .group_by(CharacterSubrace.value).all()

    for s in subraces:
        sub_dict = {}
        sub_dict["name"] = s.value
        sub_dict["count"] = 0
        for c in subrace_count:
            if c.value == s.value:
                sub_dict["count"] = c.count
                break

        for r in stat['races']:
            if r['name'] == s.race:
                r["subraces"].append(sub_dict)
                break

    stat["races"] = sorted(stat["races"], key=lambda r: r["name"])

    return stat


def get_class_table(session):
    classes = session.query(CharacterClass).all()
    class_count = session.query(CharacterClass.value, func.count(PlayerCharacterClass.primary_class).label("count")) \
        .filter(and_(Character.active == True, Character.guild_id == GUILD_ID, PlayerCharacterClass.active == True)) \
        .join(CharacterClass, PlayerCharacterClass.primary_class == CharacterClass.id) \
        .join(Character, PlayerCharacterClass.character_id == Character.id) \
        .group_by(CharacterClass.value).all()

    stat = dict()
    stat['classes'] = []

    for c in classes:
        class_dict = {}
        class_dict["name"] = c.value
        class_dict["count"] = 0
        class_dict["subclasses"] = []
        for i in class_count:
            if i.value == c.value:
                class_dict["count"] = i.count
                break
        stat["classes"].append(class_dict)

    subclasses = session.query(CharacterSubclass) \
        .join(CharacterClass, CharacterClass.id == CharacterSubclass.parent) \
        .add_columns(CharacterSubclass.id, CharacterSubclass.value, CharacterClass.value.label("char_class")).all()

    subclass_count = session.query(CharacterSubclass.value, func.count(PlayerCharacterClass.subclass).label("count")) \
        .filter(and_(Character.active == True, Character.guild_id == GUILD_ID, PlayerCharacterClass.active == True)) \
        .join(CharacterSubclass, PlayerCharacterClass.subclass == CharacterSubclass.id) \
        .join(Character, PlayerCharacterClass.character_id == Character.id) \
        .group_by(CharacterSubclass.value).all()

    for s in subclasses:
        sub_dict = {}
        sub_dict["name"] = s.value
        sub_dict["count"] = 0
        for c in subclass_count:
            if c.value == s.value:
                sub_dict["count"] = c.count
                break

        for r in stat["classes"]:
            if r["name"] == s.char_class:
                r["subclasses"].append(sub_dict)
                break

    player_count = session.query(PlayerCharacterClass.character_id,
                                 func.count(PlayerCharacterClass.character_id).label("count")) \
        .filter(and_(Character.active == True, Character.guild_id == GUILD_ID,
                     PlayerCharacterClass.active == True)) \
        .join(Character, PlayerCharacterClass.character_id == Character.id) \
        .group_by(PlayerCharacterClass.character_id).all()

    stat["classes"] = sorted(stat["classes"], key=lambda c: c["name"])

    m_dict = {}
    m_dict["name"] = "Multiclass"
    m_dict["subclasses"] = []
    m_count = 0
    for p in player_count:
        if p.count > 1:
            m_count += 1
    m_dict["count"] = m_count

    stat["classes"].append(m_dict)

    return stat

def get_item_list(session):
    blacksmith_items = session.query(BlackSmithItem.id, BlackSmithItem.name, BlackSmithType.value.label("type"),
                                     Rarity.value.label("rarity"))\
        .join(BlackSmithType, BlackSmithItem.sub_type == BlackSmithType.id)\
        .join(Rarity, BlackSmithItem.rarity == Rarity.id)

    items = []

    for i in blacksmith_items:
        i_dict = {}
        i_dict["name"] = i.name
        i_dict["id"] = i.id
        i_dict["type"] = i.type
        i_dict["rarity"] = i.rarity
        i_dict["table"] = "Blacksmith"
        items.append(i_dict)

    consumable_items = session.query(ConsumableItem.id, ConsumableItem.name, ConsumableType.value.label("type"),
                                     Rarity.value.label("rarity"))\
        .join(ConsumableType, ConsumableItem.sub_type == ConsumableType.id)\
        .join(Rarity, ConsumableItem.rarity == Rarity.id)

    for i in consumable_items:
        i_dict = {}
        i_dict["name"] = i.name
        i_dict["id"] = i.id
        i_dict["type"] = i.type
        i_dict["rarity"] = i.rarity
        i_dict["table"] = "Consumable"
        items.append(i_dict)

    scroll_items = session.query(ScrollItem.id, ScrollItem.name, Rarity.value.label("rarity"))\
        .join(Rarity, ScrollItem.rarity == Rarity.id)

    for i in scroll_items:
        i_dict = {}
        i_dict["name"] = i.name
        i_dict["id"] = i.id
        i_dict["type"] = ""
        i_dict["rarity"] = i.rarity
        i_dict["table"] = "Scroll"
        items.append(i_dict)

    wondrous_items = session.query(WondrousItem.id, WondrousItem.name, Rarity.value.label("rarity"))\
        .join(Rarity, WondrousItem.rarity == Rarity.id)

    for i in wondrous_items:
        i_dict = {}
        i_dict["name"] = i.name
        i_dict["id"] = i.id
        i_dict["type"] = ""
        i_dict["rarity"] = i.rarity
        i_dict["table"] = "Wondrous"
        items.append(i_dict)

    return items