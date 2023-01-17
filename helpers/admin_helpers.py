from flask import current_app

from models import BlackSmithItem, BlackSmithType, Rarity, ConsumableItem, ConsumableType, ScrollItem, WondrousItem, \
    CharacterRace, CharacterSubrace, CharacterClass, CharacterSubclass


def get_item_list():
    blacksmith_items = current_app.db.session.query(BlackSmithItem.id, BlackSmithItem.name, BlackSmithType.value.label("type"),
                                     Rarity.value.label("rarity")) \
        .join(BlackSmithType, BlackSmithItem.sub_type == BlackSmithType.id) \
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

    consumable_items = current_app.db.session.query(ConsumableItem.id, ConsumableItem.name, ConsumableType.value.label("type"),
                                     Rarity.value.label("rarity")) \
        .join(ConsumableType, ConsumableItem.sub_type == ConsumableType.id) \
        .join(Rarity, ConsumableItem.rarity == Rarity.id)

    for i in consumable_items:
        i_dict = {}
        i_dict["name"] = i.name
        i_dict["id"] = i.id
        i_dict["type"] = i.type
        i_dict["rarity"] = i.rarity
        i_dict["table"] = "Consumable"
        items.append(i_dict)

    scroll_items = current_app.db.session.query(ScrollItem.id, ScrollItem.name, Rarity.value.label("rarity")) \
        .join(Rarity, ScrollItem.rarity == Rarity.id)

    for i in scroll_items:
        i_dict = {}
        i_dict["name"] = i.name
        i_dict["id"] = i.id
        i_dict["type"] = ""
        i_dict["rarity"] = i.rarity
        i_dict["table"] = "Scroll"
        items.append(i_dict)

    wondrous_items = current_app.db.session.query(WondrousItem.id, WondrousItem.name, Rarity.value.label("rarity")) \
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


def get_races():
    races = current_app.db.session.query(CharacterRace)

    d_out = dict()
    d_out["parents"] = []

    for r in races:
        subraces = get_subraces(r.id)
        r_dict = {}
        r_dict['id'] = r.id
        r_dict['name'] = r.value
        r_dict['children'] = len(subraces['children'])

        d_out['parents'].append(r_dict)

    d_out["parents"] = sorted(d_out["parents"], key=lambda r: r["name"])

    return d_out


def get_subraces(race):
    subraces = current_app.db.session.query(CharacterSubrace).filter(CharacterSubrace.parent == race)

    d_out = dict()
    d_out['children'] = []

    for s in subraces:
        s_dict = {}
        s_dict['id'] = s.id
        s_dict['name'] = s.value

        d_out['children'].append(s_dict)

    d_out["children"] = sorted(d_out["children"], key=lambda r: r["name"])

    return d_out


def get_classes():
    classes = current_app.db.session.query(CharacterClass)

    d_out = dict()
    d_out["parents"] = []

    for c in classes:
        subclasses = get_subclasses(c.id)
        r_dict = {}
        r_dict['id'] = c.id
        r_dict['name'] = c.value
        r_dict['children'] = len(subclasses['children'])

        d_out['parents'].append(r_dict)

    d_out["parents"] = sorted(d_out["parents"], key=lambda r: r["name"])

    return d_out


def get_subclasses(c):
    subclasses = current_app.db.session.query(CharacterSubclass).filter(CharacterSubclass.parent == c)

    d_out = dict()
    d_out['children'] = []

    for s in subclasses:
        s_dict = {}
        s_dict['id'] = s.id
        s_dict['name'] = s.value

        d_out['children'].append(s_dict)

    d_out["children"] = sorted(d_out["children"], key=lambda r: r["name"])

    return d_out
