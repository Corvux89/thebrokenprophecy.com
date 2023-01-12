import json
from datetime import timedelta

import flask
import flask_login
from flask import Flask, render_template, redirect, url_for, session
from flask_bootstrap import Bootstrap
from flask_talisman import Talisman
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user

from constants import WEB_DEBUG, DB_URI, SECRET_KEY, USERNAME, PASSWORD
from helpers.helpers import get_race_table, get_class_table, get_item_list, get_races, get_subraces, get_classes, \
    get_subclasses
from models import *

app = Flask(__name__)

db = SQLAlchemy()

login_manager = LoginManager()

app.config["SQLALCHEMY_DATABASE_URI"] = DB_URI
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
app.secret_key = SECRET_KEY

app.config.update(
    DEBUG=WEB_DEBUG
)

admin_user = {USERNAME: {"pw": PASSWORD}}


@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=30)


@login_manager.user_loader
def user_loader(username):
    if username not in admin_user:
        return

    user = User()
    user.id = username
    return user


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    if not username or username not in admin_user:
        return
    user = User()
    user.id = username
    return user


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if flask.request.method == 'POST':
        username = flask.request.form.get('username')
        if flask.request.form.get('pw') == admin_user[username]['pw']:
            user = User()
            user.id = username
            flask_login.login_user(user)
            return redirect(url_for('admin_menu'))
    elif current_user.is_authenticated:
        return redirect(url_for('admin_menu'))
    else:
        return render_template("login.html")

    return render_template('main.html')


@app.route('/admin_menu')
@flask_login.login_required
def admin_menu():
    return render_template('/admin_pages/admin_menu.html')

@app.route('/admin/classes', methods=['GET', 'POST'])
@flask_login.login_required
def admin_classes():
    if flask.request.method == 'POST':
        c_class = CharacterClass(
            value = flask.request.form.get('name')
        )

        if c_class is not None:
            db.session.add(c_class)
            db.session.commit()

    classes = get_classes(db.session)

    return render_template('/admin_pages/admin_parent_list.html', parents=classes, label="Class", child="Subclasses",
                           path="classes")

@app.route('/admin/classes/<c_class>', methods=['GET', 'POST'])
@flask_login.login_required
def admin_subclasses(c_class):
    if flask.request.method == 'POST':
        parent = db.get_or_404(CharacterClass, c_class)
        subclass = CharacterSubclass(
            value=flask.request.form.get('name'),
            parent = parent.id
        )

        if subclass is not None:
            db.session.add(subclass)
            db.session.commit()

    subclasses = get_subclasses(db.session, c_class)
    p_class = db.session.query(CharacterClass).filter(CharacterClass.id == c_class).first()

    return render_template('/admin_pages/admin_child_list.html', children=subclasses, parent="class", label="Subclass",
                           path="classes", parent_name=p_class.value, parent_id=p_class.id)

@app.route('/admin/classes/Subclass', methods=['POST'])
@flask_login.login_required
def admin_subclass_edit():
    if flask.request.method == 'POST':
        s_class = db.get_or_404(CharacterSubclass, flask.request.form.get('childID'))
        if flask.request.form.get('update') is not None:
            s_class.value = flask.request.form.get('childName')

            if s_class is not None:
                db.session.add(s_class)
                db.session.commit()

        elif flask.request.form.get('delete') is not None:
            c_classes = db.session.query(PlayerCharacterClass).filter(PlayerCharacterClass.subclass == s_class.id)

            if s_class is not None:

                for c in c_classes:
                    c.subclass = None
                    db.session.add(c)

                db.session.delete(s_class)
                db.session.commit()

    return redirect(f'/admin/classes/{s_class.parent}')


@app.route('/admin/classes/delete', methods=['POST'])
@flask_login.login_required
def admin_class_delete():
    if flask.request.method == 'POST':
        c_class = db.get_or_404(CharacterClass, flask.request.form.get('parentID'))
        subclasses = db.session.query(CharacterSubclass).filter(CharacterSubclass.parent == c_class.id)
        c_classes = db.session.query(PlayerCharacterClass).filter(PlayerCharacterClass.primary_class == c_class.id)

        for c in c_classes:
            c.primary_class = 13  # Default to a Wizard
            c.subclass = None
            db.session.add(c)

        for s in subclasses:
            db.session.delete(s)

        db.session.delete(c_class)
        db.session.commit()

        return redirect(url_for('admin_classes'))



@app.route('/admin/races', methods=['GET', 'POST'])
@flask_login.login_required
def admin_races():
    if flask.request.method == 'POST':
        race = CharacterRace(
            value=flask.request.form.get('name')
        )
        if race is not None:
            db.session.add(race)
            db.session.commit()

    races = get_races(db.session)

    return render_template('/admin_pages/admin_parent_list.html', parents=races, label="Race", child="Subraces",
                           path="races")


@app.route('/admin/races/<race>', methods=['GET', 'POST'])
@flask_login.login_required
def admin_subraces(race):
    if flask.request.method == 'POST':
        parent = db.get_or_404(CharacterRace, race)
        subrace = CharacterSubrace(
            value=flask.request.form.get('name'),
            parent=parent.id
        )

        if subrace is not None:
            db.session.add(subrace)
            db.session.commit()

    subraces = get_subraces(db.session, race)
    race = db.session.query(CharacterRace).filter(CharacterRace.id == race).first()

    return render_template('/admin_pages/admin_child_list.html', children=subraces, parent="race", label="Subrace",
                           path="races", parent_name=race.value, parent_id=race.id)


@app.route('/admin/races/Subrace', methods=['POST'])
@flask_login.login_required
def admin_subrace_edit():
    if flask.request.method == 'POST':
        s_race = db.get_or_404(CharacterSubrace, flask.request.form.get('childID'))
        if flask.request.form.get('update') is not None:
            s_race.value = flask.request.form.get('childName')

            if s_race is not None:
                db.session.add(s_race)
                db.session.commit()

        elif flask.request.form.get('delete') is not None:
            characters = db.session.query(Character).filter(Character.subrace == s_race.id)

            if s_race is not None:
                for c in characters:
                    c.subrace = None
                    db.session.add(c)

                db.session.delete(s_race)
                db.session.commit()

    return redirect(f'/admin/races/{s_race.parent}')


@app.route('/admin/races/delete', methods=['POST'])
@flask_login.login_required
def admin_race_delete():
    if flask.request.method == 'POST':
        race = db.get_or_404(CharacterRace, flask.request.form.get('parentID'))
        subraces = db.session.query(CharacterSubrace).filter(CharacterSubrace.parent == race.id)
        characters = db.session.query(Character).filter(Character.race == race.id)

        for c in characters:
            c.race = 21  # Default to human
            c.subrace = None
            db.session.add(c)

        for s in subraces:
            db.session.delete(s)

        db.session.delete(race)
        db.session.commit()

        return redirect(url_for('admin_races'))


@app.route('/admin/items')
@flask_login.login_required
def item_list():
    items = get_item_list(db.session)

    return render_template('/admin_pages/admin_item_list.html', items=items)


@app.route('/admin/items/<table>/<id>', methods=['GET', 'POST'])
@flask_login.login_required
def item_modify(table, id):
    if flask.request.method == 'POST':
        if table.upper() == "BLACKSMITH":
            item_update = db.get_or_404(BlackSmithItem, id)
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
            item_update = db.get_or_404(ConsumableItem, id)
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
            item_update = db.get_or_404(ScrollItem, id)
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
            item_update = db.get_or_404(WondrousItem, id)
            item_update.name = flask.request.form.get('name')
            item_update.rarity = flask.request.form.get('rarity')
            item_update.cost = flask.request.form.get('cost')
            item_update.attunement = True if flask.request.form.get('attunement') == "" else False
            item_update.seeking_only = True if flask.request.form.get('seeking') == "" else False
            item_update.source = None if flask.request.form.get('source') == "None" else \
                flask.request.form.get('source')
            item_update.notes = None if flask.request.form.get('notes') == "None" else flask.request.form.get('notes')

        if item_update is not None:
            db.session.add(item_update)
            db.session.commit()
        return redirect(url_for('item_list'))

    schools = None
    sub_type = None
    classes = None
    item = None

    if table.upper() == "BLACKSMITH":
        item = db.session.query(BlackSmithItem).filter(BlackSmithItem.id == id).first()
        sub_type = db.session.query(BlackSmithType).all()
    elif table.upper() == "CONSUMABLE":
        item = db.session.query(ConsumableItem).filter(ConsumableItem.id == id).first()
        sub_type = db.session.query(ConsumableType).all()
    elif table.upper() == "SCROLL":
        item = db.session.query(ScrollItem).filter(ScrollItem.id == id).first()
        schools = db.session.query(MagicSchool).all()
        classes = db.session.query(CharacterClass).all()
    elif table.upper() == "WONDROUS":
        item = db.session.query(WondrousItem).filter(WondrousItem.id == id).first()

    rarity = db.session.query(Rarity).all()
    return render_template('/admin_pages/admin_item_edit.html', item=item, table=table, subs=sub_type, rarity=rarity,
                           schools=schools, classes=classes)


@app.route('/admin/items/delete_item/<table>/<id>', methods=['POST'])
@flask_login.login_required
def delete_item(table, id):
    if flask.request.method == "POST":
        if table.upper() == "BLACKSMITH":
            item = db.session.query(BlackSmithItem).filter(BlackSmithItem.id == id).first()
        elif table.upper() == "CONSUMABLE":
            item = db.session.query(ConsumableItem).filter(ConsumableItem.id == id).first()
        elif table.upper() == "SCROLL":
            item = db.session.query(ScrollItem).filter(ScrollItem.id == id).first()
        elif table.upper() == "WONDROUS":
            item = db.session.query(WondrousItem).filter(WondrousItem.id == id).first()

        if item is not None:
            db.session.delete(item)
            db.session.commit()

    return redirect(url_for('item_list'))


@app.route('/admin/items/add_item')
@flask_login.login_required
def select_table():
    tables = ['Blacksmith', 'Consumable', 'Scroll', 'Wondrous']
    return render_template('/admin_pages/admin_item_table.html', tables=tables)


@app.route('/admin/items/add_item/<table>', methods=["GET", "POST"])
@flask_login.login_required
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
                source=None if flask.request.form.get('source') == "None" else \
                    flask.request.form.get('source'),
                notes=None if flask.request.form.get('notes') == "None" else \
                    flask.request.form.get('notes'))

        elif table.upper() == "CONSUMABLE":
            item = ConsumableItem(
                name=flask.request.form.get('name'),
                sub_type=flask.request.form.get('sub-type'),
                rarity=flask.request.form.get('rarity'),
                cost=flask.request.form.get('cost'),
                attunement=True if flask.request.form.get('attunement') == "" else False,
                seeking_only=True if flask.request.form.get('seeking') == "" else False,
                source=None if flask.request.form.get('source') == "None" else \
                    flask.request.form.get('source'),
                notes=None if flask.request.form.get('notes') == "None" else \
                    flask.request.form.get('notes'))

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
                source=None if flask.request.form.get('source') == "None" else \
                    flask.request.form.get('source'),
                notes=None if flask.request.form.get('notes') == "None" else \
                    flask.request.form.get('notes'))

        elif table.upper() == "WONDROUS":
            item = WondrousItem(
                name=flask.request.form.get('name'),
                rarity=flask.request.form.get('rarity'),
                cost=flask.request.form.get('cost'),
                attunement=True if flask.request.form.get('attunement') == "" else False,
                seeking_only=True if flask.request.form.get('seeking') == "" else False,
                source=None if flask.request.form.get('source') == "None" else \
                    flask.request.form.get('source'),
                notes=None if flask.request.form.get('notes') == "None" else \
                    flask.request.form.get('notes'))

        if item is not None:
            db.session.add(item)
            db.session.commit()
            return redirect(f'/admin/items/{table}/{item.id}')
        else:
            return redirect(url_for('item_list'))

    rarity = db.session.query(Rarity).all()
    sub_type = None
    classes = None
    schools = None
    if table.upper() == "BLACKSMITH":
        sub_type = db.session.query(BlackSmithType).all()
    elif table.upper() == "CONSUMABLE":
        sub_type = db.session.query(ConsumableType).all()
    elif table.upper() == "SCROLL":
        classes = db.session.query(CharacterClass).all()
        schools = db.session.query(MagicSchool).all()

    return render_template('/admin_pages/admin_item_add.html', table=table, subs=sub_type, rarity=rarity,
                           classes=classes, schools=schools)


@app.route('/')
@app.route('/home')
def homepage():
    return render_template("main.html")


@app.route('/credits')
def credits():
    return render_template('credits.html')


@app.route('/server_stats')
def census():
    race_data = get_race_table(db.session)
    class_data = get_class_table(db.session)

    return render_template('server_stats.html', race_data=race_data, class_data=class_data)


@app.route('/commands')
def bot():
    f = open('json/commands.json')
    commands = json.load(f)
    return render_template('commands.html', commands=commands['category'])


@app.route('/commands/<role>')
def player_commands(role):
    f = open('json/commands.json')
    commands = json.load(f)
    filter_commands = {}
    filter_commands['category'] = []

    for c in commands['category']:
        if "role" in c and role in c["role"]:
            filter_commands['category'].append(c)

    return render_template('commands.html', commands=filter_commands['category'], role=role)


@app.route('/factions')
def faction_list():
    f = open('json/factions.json', encoding="utf8")
    guild = json.load(f)
    return render_template('faction_list.html', guild=guild)


csp = {
    'default-src': [
        '\'self\'',
        'https://docs.google.com',
        'https://code.jquery.com/'
        'https://cdn.jsdelivr.net/npm/',
        'https://www.googletagmanager.com/',
        'https://analytics.google.com/',
        'https://www.google-analytics.com/',
        'https://use.fontawesome.com',
        'https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.2/font/bootstrap-icons.css',
        'https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.2/font/fonts/',
    ],
    'script-src': [
        '\'self\'',
        'https://cdn.jsdelivr.net/',
        'https://www.googletagmanager.com/',
        'https://ajax.googleapis.com',
        'https://cdnjs.cloudflare.com/',
        'https://cdn.datatables.net/1.13.1/js/jquery.dataTables.js'
    ],
    'img-src': [
        '*',
        'data:'
    ],
    'style-src': [
        '\'self\'',
        'https://cdn.jsdelivr.net/',
        'https://use.fontawesome.com',
        'https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.2/font/bootstrap-icons.css',
        'https://cdn.datatables.net/1.13.1/css/jquery.dataTables.css'
    ],
    'script-src-elem': [
        '\'self\'',
        'https://cdnjs.cloudflare.com/',
        'https://cdn.jsdelivr.net/',
        'https://ajax.googleapis.com',
        'https://cdn.datatables.net/1.13.1/js/jquery.dataTables.js'
    ]
}

Bootstrap(app)
talisman = Talisman(
    app,
    content_security_policy=csp,
    content_security_policy_nonce_in=['script-src', 'script-src-elem']
)

db.init_app(app)
login_manager.init_app(app)

if __name__ == "__main__":
    app.run()
