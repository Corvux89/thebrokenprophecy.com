from flask import current_app
from sqlalchemy import literal, union, select
from werkzeug.datastructures import ImmutableMultiDict

from models import BlackSmithItem, BlackSmithType, Rarity, ConsumableItem, ConsumableType, ScrollItem, WondrousItem, \
    CharacterRace, CharacterSubrace, CharacterClass, CharacterSubclass, BPLog, Character, Activity, MagicSchool


def get_item_list():
    s1 = select(BlackSmithItem.id,
                BlackSmithItem.name,
                BlackSmithItem.cost,
                BlackSmithType.value.label('type'),
                Rarity.value.label('rarity'),
                literal('Blacksmith').label('table')) \
        .join(BlackSmithType, BlackSmithItem.sub_type == BlackSmithType.id) \
        .join(Rarity, BlackSmithItem.rarity == Rarity.id)

    s2 = select(ConsumableItem.id,
                ConsumableItem.name,
                ConsumableItem.cost,
                ConsumableType.value.label('type'),
                Rarity.value.label('rarity'),
                literal('Consumable').label('table')) \
        .join(ConsumableType, ConsumableItem.sub_type == ConsumableType.id) \
        .join(Rarity, ConsumableItem.rarity == Rarity.id)

    s3 = select(ScrollItem.id,
                ScrollItem.name,
                ScrollItem.cost,
                literal('').label('type'),
                Rarity.value.label('rarity'),
                literal('Scroll').label('table')) \
        .join(Rarity, ScrollItem.rarity == Rarity.id)

    s4 = select(WondrousItem.id,
                WondrousItem.name,
                WondrousItem.cost,
                literal('').label('type'),
                Rarity.value.label('rarity'),
                literal('Wondrous').label('table')) \
        .join(Rarity, WondrousItem.rarity == Rarity.id)

    u = union(s1, s2, s3, s4).alias('items')

    vals = current_app.db.session.query(u)

    items = [{"name": v.name, "id": v.id, "cost": v.cost, "type": v.type, "rarity": v.rarity, "table": v.table} for v in
             vals]

    return items


def get_races():
    races = current_app.db.session.query(CharacterRace)

    d_out = dict()
    d_out["parents"] = [{"id": r.id, "name": r.value, "children": len(get_subraces(r.id)['children'])} for r in races]

    d_out["parents"] = sorted(d_out["parents"], key=lambda r: r["name"])

    return d_out


def get_subraces(race):
    subraces = current_app.db.session.query(CharacterSubrace).filter(CharacterSubrace.parent == race)

    d_out = dict()
    d_out['children'] = [{"id": s.id, "name": s.value} for s in subraces]

    d_out["children"] = sorted(d_out["children"], key=lambda r: r["name"])

    return d_out


def get_classes():
    classes = current_app.db.session.query(CharacterClass)

    d_out = dict()
    d_out["parents"] = [{"id": c.id, "name": c.value, "children": len(get_subclasses(c.id)['children'])} for c in
                        classes]

    d_out["parents"] = sorted(d_out["parents"], key=lambda r: r["name"])

    return d_out


def get_subclasses(c):
    subclasses = current_app.db.session.query(CharacterSubclass).filter(CharacterSubclass.parent == c)

    d_out = dict()
    d_out['children'] = [{"id": s.id, "name": s.value} for s in subclasses]

    d_out["children"] = sorted(d_out["children"], key=lambda r: r["name"])

    return d_out


def get_logs():
    db_logs = current_app.db.session.query(BPLog.id,
                                           BPLog.xp,
                                           BPLog.gold,
                                           BPLog.server_xp,
                                           BPLog.created_ts.label('timestamp'),
                                           Character.name,
                                           Activity.value.label('activity'),
                                           BPLog.notes,
                                           BPLog.invalid) \
        .join(Character, BPLog.character_id == Character.id) \
        .join(Activity, BPLog.activity == Activity.id) \
        .order_by(BPLog.id.desc()).limit(1000).all()

    logs = [{"id": l.id,
             "xp": l.xp,
             "gold": l.gold,
             "server_xp": l.server_xp,
             "timestamp": l.timestamp.strftime("%m/%d/%Y %H:%M:%S"),
             "name": l.name,
             "activity": l.activity,
             "notes": l.notes,
             "invalid": l.invalid} for l in db_logs]

    return logs

def get_table(str):
    return BlackSmithItem if str.lower() == "blacksmith" else ConsumableItem if str.lower() == "consumable" else ScrollItem if str.lower() == "scroll" else WondrousItem if str.lower() == "wondrous" else None

def get_subtype(str):
    return current_app.db.session.query(BlackSmithType).all() if str.lower() == "blacksmith" else current_app.db.session.query(ConsumableType).all() if str.lower() == "consumable" else None

def get_table_items(table, id):
    sub_type = get_subtype(table)
    table = get_table(table)

    item = current_app.db.session.query(table).filter(table.id == id).first()
    schools = current_app.db.session.query(MagicSchool).all() if hasattr(item, "school") else None
    classes = current_app.db.session.query(CharacterClass).all() if hasattr(item, "classes") else None

    return item, sub_type, schools, classes

def update_item(table, id, form: ImmutableMultiDict[str, str]):
    table=get_table(table)
    item = current_app.db.session.query(table).filter(table.id == id).first()

    if not item:
        return

    item.name = form.get('name')
    item.rarity = int(form.get('rarity'))
    item.cost = int(form.get('cost'))
    item.source = form.get('source') or None
    item.notes = form.get('notes') or None

    if hasattr(item, 'sub_type'):
        item.sub_type = int(form.get('sub-type'))

    if hasattr(item, 'item_modifier'):
        item.item_modifier = bool(form.get('item-modifier', default=False))

    if hasattr(item, 'attunement'):
        item.attunement = bool(form.get('attunement', default=False))

    if hasattr(item, 'seeking_only'):
        item.seeking_only = bool(form.get('seeking', default=False))

    if hasattr(item, "school"):
        item.school = int(form.get('school'))

    if hasattr(item, "level"):
        item.level = int(form.get('level'))

    if hasattr(item, "classes"):
        item.classes = [int(i[1]) for i in form.items() if 'class' in i[0]]

    current_app.db.session.add(item)
    current_app.db.session.commit()

def add_item(table, form: ImmutableMultiDict[str, str]):
    if table.lower() == 'blacksmith':
        item = BlackSmithItem(
            name=form.get('name'),
            sub_type=int(form.get('sub-type')),
            rarity=int(form.get('rarity')),
            cost=int(form.get('cost')),
            item_modifier=bool(form.get('item-modifier', default=False)),
            attunement=bool(form.get('attunement', default=False)),
            seeking_only=bool(form.get('seeking', default=False)),
            source=form.get('source') or None,
            notes=form.get('notes') or None
        )

    elif table.lower() == 'consumable':
        item = ConsumableItem(
            name=form.get('name'),
            sub_type=form.get('sub-type'),
            rarity=int(form.get('rarity')),
            cost=int(form.get('cost')),
            attunement=bool(form.get('attunement', default=False)),
            seeking_only=bool(form.get('seeking', default=False)),
            source=form.get('source') or None,
            notes=form.get('notes') or None
        )

    elif table.lower() == 'scroll':
        item = ScrollItem(
            name=form.get('name'),
            rarity=int(form.get('rarity')),
            cost=int(form.get('cost')),
            level=int(form.get('level')),
            school=int(form.get('school')),
            classes=[int(i[1]) for i in form.items() if 'class' in i[0]],
            source=form.get('source') or None,
            notes=form.get('notes') or None
        )

    elif table.lower() == 'wondrous':
        item = WondrousItem(
            name=fomr.get('name'),
            rarity=int(form.get('rarity')),
            cost=int(form.get('cost')),
            attunement=bool(form.get('attunement', default=False)),
            seeking_only=bool(form.get('seeking', default=False)),
            source=form.get('source') or None,
            notes=form.get('notes') or None
        )

    if item is not None:
        current_app.db.session.add(item)
        current_app.db.session.commit()

