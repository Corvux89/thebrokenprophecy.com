import flask
import flask_login
from flask import Blueprint, current_app, redirect, url_for, render_template, request
from flask_login import current_user

from helpers import get_item_list, get_races, get_subraces, get_classes, get_subclasses, is_admin
from models import CharacterClass, CharacterSubclass, PlayerCharacterClass, CharacterRace, CharacterSubrace, \
    Character, BlackSmithItem, ConsumableItem, ScrollItem, WondrousItem, BlackSmithType, ConsumableType, MagicSchool, \
    Rarity

admin_blueprint = Blueprint("admin", __name__)

@admin_blueprint.before_request
@is_admin
def before_request():
    pass


@admin_blueprint.route('/')
@admin_blueprint.route('/<path>')
@admin_blueprint.route('/<path>/<sub>')
def admin_menu(path = None, sub=None):
    if sub:
        return redirect(f'{url_for("admin.admin_menu")}/{path}/{sub}')
    elif path:
        return redirect(f'{url_for("admin.admin_menu")}/{path}')
    else:
        return render_template('/admin_pages/admin_menu.html')



# Character Class Administration
@admin_blueprint.route('/classes', methods=['GET', 'POST'])
def admin_classes():
    if flask.request.method == 'POST':
        c_class = CharacterClass(
            value=flask.request.form.get('name')
        )

        if c_class is not None:
            current_app.db.session.add(c_class)
            current_app.db.session.commit()

    classes = get_classes()

    return render_template('/admin_pages/admin_parent_list.html', parents=classes, label="Class", child="Subclasses",
                           path="classes")


@admin_blueprint.route('/classes/<c_class>', methods=['GET', 'POST'])
def admin_sublasses(c_class):
    if flask.request.method == 'POST':
        parent = current_app.db.get_or_404(CharacterClass, c_class)
        subclass = CharacterSubclass(
            value=flask.request.form.get('name'),
            parent=parent.id
        )

        if subclass is not None:
            current_app.db.session.add(subclass)
            current_app.db.session.commit()

    subclasses = get_subclasses(c_class)
    p_class = current_app.db.session.query(CharacterClass).filter(CharacterClass.id == c_class).first()

    return render_template('/admin_pages/admin_child_list.html', children=subclasses, parent="class", label="Subclass",
                           path="classes", parent_name=p_class.value, parent_id=p_class.id)


@admin_blueprint.route('/classes/Subclass', methods=['POST'])
def admin_subclass_edit():
    if flask.request.method == 'POST':
        s_class = current_app.db.get_or_404(CharacterSubclass, flask.request.form.get('childID'))
        if flask.request.form.get('update') is not None:
            s_class.value = flask.request.form.get('childName')

            if s_class is not None:
                current_app.db.session.add(s_class)
                current_app.db.session.commit()

        elif flask.request.form.get('delete') is not None:
            c_classes = current_app.db.session.query(PlayerCharacterClass).filter(
                PlayerCharacterClass.subclass == s_class.id)

            if s_class is not None:

                for c in c_classes:
                    c.subclass = None
                    current_app.db.session.add(c)

                current_app.db.session.delete(s_class)
                current_app.db.session.commit()

    return redirect(f'{url_for("admin.admin_classes")}/{s_class.parent}')


@admin_blueprint.route('/classes/delete', methods=['POST'])
def admin_class_delete():
    if flask.request.method == 'POST':
        c_class = current_app.db.get_or_404(CharacterClass, flask.request.form.get('parentID'))
        subclasses = current_app.db.session.query(CharacterSubclass).filter(CharacterSubclass.parent == c_class.id)
        c_classes = current_app.db.session.query(PlayerCharacterClass).filter(
            PlayerCharacterClass.primary_class == c_class.id)

        for c in c_classes:
            c.primary_class = 13  # Default to a Wizard
            c.subclass = None
            current_app.db.session.add(c)

        for s in subclasses:
            current_app.db.session.delete(s)

        current_app.db.session.delete(c_class)
        current_app.db.session.commit()

        return redirect(url_for('admin.admin_classes'))


# Character Race Administration
@admin_blueprint.route('/races', methods=['GET', 'POST'])
def admin_races():
    if flask.request.method == 'POST':
        race = CharacterRace(
            value=flask.request.form.get('name')
        )
        if race is not None:
            current_app.db.session.add(race)
            current_app.db.session.commit()

    races = get_races()

    return render_template('/admin_pages/admin_parent_list.html', parents=races, label="Race", child="Subraces",
                           path="races")


@admin_blueprint.route('/races/<race>', methods=['GET', 'POST'])
def admin_subraces(race):
    if flask.request.method == 'POST':
        parent = current_app.db.get_or_404(CharacterRace, race)
        subrace = CharacterSubrace(
            value=flask.request.form.get('name'),
            parent=parent.id
        )

        if subrace is not None:
            current_app.db.session.add(subrace)
            current_app.db.session.commit()

    subraces = get_subraces(race)
    race = current_app.db.session.query(CharacterRace).filter(CharacterRace.id == race).first()

    return render_template('/admin_pages/admin_child_list.html', children=subraces, parent="race", label="Subrace",
                           path="races", parent_name=race.value, parent_id=race.id)


@admin_blueprint.route('/races/Subrace', methods=['POST'])
def admin_subrace_edit():
    if flask.request.method == 'POST':
        s_race = current_app.db.get_or_404(CharacterSubrace, flask.request.form.get('childID'))
        if flask.request.form.get('update') is not None:
            s_race.value = flask.request.form.get('childName')

            if s_race is not None:
                current_app.db.session.add(s_race)
                current_app.db.session.commit()

        elif flask.request.form.get('delete') is not None:
            characters = current_app.db.session.query(Character).filter(Character.subrace == s_race.id)

            if s_race is not None:
                for c in characters:
                    c.subrace = None
                    current_app.db.session.add(c)

                current_app.db.session.delete(s_race)
                current_app.db.session.commit()

    return redirect(f'{url_for("admin.admin_races")}/{s_race.parent}')


@admin_blueprint.route('/races/delete', methods=['POST'])
def admin_race_delete():
    if flask.request.method == 'POST':
        race = current_app.db.get_or_404(CharacterRace, flask.request.form.get('parentID'))
        subraces = current_app.db.session.query(CharacterSubrace).filter(CharacterSubrace.parent == race.id)
        characters = current_app.db.session.query(Character).filter(Character.race == race.id)

        for c in characters:
            c.race = 21  # Default to human
            c.subrace = None
            current_app.db.session.add(c)

        for s in subraces:
            current_app.db.session.delete(s)

        current_app.db.session.delete(race)
        current_app.db.session.commit()

        return redirect(url_for('admin.admin_races'))


# Item Administration
@admin_blueprint.route('/items')
def item_list():
    items = get_item_list()

    return render_template('/admin_pages/admin_item_list.html', items=items)


@admin_blueprint.route('/items/<table>/<id>', methods=['GET', 'POST'])
def item_modify(table, id):
    if flask.request.method == 'POST':
        if table.upper() == "BLACKSMITH":
            item_update = current_app.db.get_or_404(BlackSmithItem, id)
            item_update.name = flask.request.form.get('name')
            item_update.sub_type = flask.request.form.get('sub-type')
            item_update.rarity = flask.request.form.get('rarity')
            item_update.cost = flask.request.form.get('cost')
            item_update.item_modifier = True if flask.request.form.get('item-modifier') == "" else False
            item_update.attunement = True if flask.request.form.get('attunement') == "" else False
            item_update.seeking_only = True if flask.request.form.get('seeking') == "" else False
            item_update.source = None if flask.request.form.get('source') == "None" else \
                flask.request.form.get('source')
            item_update.notes = None if flask.request.form.get('notes') == "None" else flask.request.form.get('notes')

        elif table.upper() == "CONSUMABLE":
            item_update = current_app.db.get_or_404(ConsumableItem, id)
            item_update.name = flask.request.form.get('name')
            item_update.sub_type = flask.request.form.get('sub-type')
            item_update.rarity = flask.request.form.get('rarity')
            item_update.cost = flask.request.form.get('cost')
            item_update.attunement = True if flask.request.form.get('attunement') == "" else False
            item_update.seeking_only = True if flask.request.form.get('seeking') == "" else False
            item_update.source = None if flask.request.form.get('source') == "None" else \
                flask.request.form.get('source')
            item_update.notes = None if flask.request.form.get('notes') == "None" else flask.request.form.get('notes')

        elif table.upper() == "SCROLL":
            item_update = current_app.db.get_or_404(ScrollItem, id)
            item_update.name = flask.request.form.get('name')
            item_update.rarity = flask.request.form.get('rarity')
            item_update.cost = flask.request.form.get('cost')
            item_update.source = None if flask.request.form.get('source') == "None" else \
                flask.request.form.get('source')
            item_update.level = flask.request.form.get('level')
            item_update.school = flask.request.form.get('school')
            item_update.notes = None if flask.request.form.get('notes') == "None" else flask.request.form.get('notes')

            classes = []
            for i in flask.request.form.items():
                if 'class' in i[0]:
                    classes.append(i[1])

            item_update.classes = classes

        elif table.upper() == "WONDROUS":
            item_update = current_app.db.get_or_404(WondrousItem, id)
            item_update.name = flask.request.form.get('name')
            item_update.rarity = flask.request.form.get('rarity')
            item_update.cost = flask.request.form.get('cost')
            item_update.attunement = True if flask.request.form.get('attunement') == "" else False
            item_update.seeking_only = True if flask.request.form.get('seeking') == "" else False
            item_update.source = None if flask.request.form.get('source') == "None" else \
                flask.request.form.get('source')
            item_update.notes = None if flask.request.form.get('notes') == "None" else flask.request.form.get('notes')

        if item_update is not None:
            current_app.db.session.add(item_update)
            current_app.db.session.commit()
        return redirect(url_for('admin.item_list'))

    schools = None
    sub_type = None
    classes = None
    item = None

    if table.upper() == "BLACKSMITH":
        item = current_app.db.session.query(BlackSmithItem).filter(BlackSmithItem.id == id).first()
        sub_type = current_app.db.session.query(BlackSmithType).all()
    elif table.upper() == "CONSUMABLE":
        item = current_app.db.session.query(ConsumableItem).filter(ConsumableItem.id == id).first()
        sub_type = current_app.db.session.query(ConsumableType).all()
    elif table.upper() == "SCROLL":
        item = current_app.db.session.query(ScrollItem).filter(ScrollItem.id == id).first()
        schools = current_app.db.session.query(MagicSchool).all()
        classes = current_app.db.session.query(CharacterClass).all()
    elif table.upper() == "WONDROUS":
        item = current_app.db.session.query(WondrousItem).filter(WondrousItem.id == id).first()

    rarity = current_app.db.session.query(Rarity).all()
    return render_template('/admin_pages/admin_item_edit.html', item=item, table=table, subs=sub_type, rarity=rarity,
                           schools=schools, classes=classes)


@admin_blueprint.route('/items/delete_item/<table>/<id>', methods=['POST'])
def delete_item(table, id):
    if flask.request.method == "POST":
        if table.upper() == "BLACKSMITH":
            item = current_app.db.session.query(BlackSmithItem).filter(BlackSmithItem.id == id).first()
        elif table.upper() == "CONSUMABLE":
            item = current_app.db.session.query(ConsumableItem).filter(ConsumableItem.id == id).first()
        elif table.upper() == "SCROLL":
            item = current_app.db.session.query(ScrollItem).filter(ScrollItem.id == id).first()
        elif table.upper() == "WONDROUS":
            item = current_app.db.session.query(WondrousItem).filter(WondrousItem.id == id).first()

        if item is not None:
            current_app.db.session.delete(item)
            current_app.db.session.commit()

    return redirect(url_for('admin.item_list'))


@admin_blueprint.route('/items/add_item')
def select_table():
    tables = ['Blacksmith', 'Consumable', 'Scroll', 'Wondrous']
    return render_template('/admin_pages/admin_item_table.html', tables=tables)


@admin_blueprint.route('/items/add_item/<table>', methods=['GET', 'POST'])
def add_item(table):
    if flask.request.method == "POST":
        if table.upper() == "BLACKSMITH":
            item = BlackSmithItem(
                name=flask.request.form.get('name'),
                sub_type=flask.request.form.get('sub-type'),
                rarity=flask.request.form.get('rarity'),
                cost=flask.request.form.get('cost'),
                item_modifier=True if flask.request.form.get('item-modifier') == "" else False,
                attunement=True if flask.request.form.get('attunement') == "" else False,
                seeking_only=True if flask.request.form.get('seeking') == "" else False,
                source=None if flask.request.form.get('source') == "None" else flask.request.form.get('source'),
                notes=None if flask.request.form.get('notes') == "None" else flask.request.form.get('notes'))

        elif table.upper() == "CONSUMABLE":
            item = ConsumableItem(
                name=flask.request.form.get('name'),
                sub_type=flask.request.form.get('sub-type'),
                rarity=flask.request.form.get('rarity'),
                cost=flask.request.form.get('cost'),
                attunement=True if flask.request.form.get('attunement') == "" else False,
                seeking_only=True if flask.request.form.get('seeking') == "" else False,
                source=None if flask.request.form.get('source') == "None" else flask.request.form.get('source'),
                notes=None if flask.request.form.get('notes') == "None" else flask.request.form.get('notes'))

        elif table.upper() == "SCROLL":
            classes = []
            for i in flask.request.form.items():
                if 'class' in i[0]:
                    classes.append(i[1])

            item = ScrollItem(
                name=flask.request.form.get('name'),
                rarity=flask.request.form.get('rarity'),
                cost=flask.request.form.get('cost'),
                level=flask.request.form.get('level'),
                school=flask.request.form.get('school'),
                classes=classes,
                source=None if flask.request.form.get('source') == "None" else flask.request.form.get('source'),
                notes=None if flask.request.form.get('notes') == "None" else flask.request.form.get('notes'))

        elif table.upper() == "WONDROUS":
            item = WondrousItem(
                name=flask.request.form.get('name'),
                rarity=flask.request.form.get('rarity'),
                cost=flask.request.form.get('cost'),
                attunement=True if flask.request.form.get('attunement') == "" else False,
                seeking_only=True if flask.request.form.get('seeking') == "" else False,
                source=None if flask.request.form.get('source') == "None" else flask.request.form.get('source'),
                notes=None if flask.request.form.get('notes') == "None" else flask.request.form.get('notes'))

        if item is not None:
            current_app.db.session.add(item)
            current_app.db.session.commit()
            return redirect(f'{url_for("admin.item_list")}')
        else:
            return redirect(url_for('admin.item_list'))

    rarity = current_app.db.session.query(Rarity).all()
    sub_type = None
    classes = None
    schools = None
    if table.upper() == "BLACKSMITH":
        sub_type = current_app.db.session.query(BlackSmithType).all()
    elif table.upper() == "CONSUMABLE":
        sub_type = current_app.db.session.query(ConsumableType).all()
    elif table.upper() == "SCROLL":
        classes = current_app.db.session.query(CharacterClass).all()
        schools = current_app.db.session.query(MagicSchool).all()

    return render_template('/admin_pages/admin_item_add.html', table=table, subs=sub_type, rarity=rarity,
                           classes=classes, schools=schools)
