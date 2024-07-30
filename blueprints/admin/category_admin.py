import flask
from flask import Blueprint, current_app, render_template
from flask_sqlalchemy import SQLAlchemy

from helpers import get_subclasses, get_classes, get_races, get_subraces
from models import CharacterClass, CharacterSubclass, PlayerCharacterClass, CharacterRace, CharacterSubrace, Character, \
    ScrollItem

cat_admin_blueprint = Blueprint("cat_admin", __name__)

# Character Classes and Subclasses
@cat_admin_blueprint.route('/classes', methods=['GET', 'POST'])
def admin_classes():
    if flask.request.method == 'POST':
        db: SQLAlchemy = current_app.config.get('DB')
        if flask.request.form.get('delete') and (c_class := db.get_or_404(CharacterClass, flask.request.form.get('parentID'))):
            subclasses = db.session.query(CharacterSubclass).filter(CharacterSubclass.parent == c_class.id)
            player_classes = db.session.query(PlayerCharacterClass).filter(PlayerCharacterClass.primary_class == c_class.id)
            items = db.session.query(ScrollItem).filter(ScrollItem.classes.any(c_class.id))
            for c in player_classes:
                c.primary_class = 13  # Wizard
                c.subclass = None
                current_app.db.session.add(c)

            for i in items:
                i.classes.remove(c_class.id)
                db.session.add(i)

            _ = [db.session.delete(s) for s in subclasses]

            db.session.delete(c_class)
        elif flask.request.form.get('name') and (c_class := CharacterClass(value=flask.request.form.get('name'))):
            db.session.add(c_class)

        db.session.commit()

    return render_template('/admin_pages/cat_admin/parent_list.html', parents=get_classes(), parent_label="class",
                           child_label="subclass", href="admin.cat_admin.admin_subclasses")

@cat_admin_blueprint.route('/classes/<parent>', methods=['GET', 'POST'])
def admin_subclasses(parent):
    db: SQLAlchemy = current_app.config.get('DB')
    parent = db.get_or_404(CharacterClass, parent)

    if flask.request.method == 'POST':
        if not flask.request.form.get('childID') and (subclass := CharacterSubclass(value=flask.request.form.get('name'), parent=parent.id)):
            db.session.add(subclass)
        elif subclass := db.get_or_404(CharacterSubclass, flask.request.form.get('childID')):
            if flask.request.form.get('update'):
                subclass.value = flask.request.form.get('childName')
                db.session.add(subclass)
            elif flask.request.form.get('delete'):
                db.session.delete(subclass)

        db.session.commit()

    return render_template('/admin_pages/cat_admin/child_list.html', children=get_subclasses((parent.id)),
                           parent_label="class", label="subclass", parent=parent,
                           parent_url="admin.cat_admin.admin_classes")

# Character Races and Subraces
@cat_admin_blueprint.route('/races', methods=['GET', 'POST'])
def admin_races():
    if flask.request.method == 'POST':
        db: SQLAlchemy = current_app.config.get('DB')
        if flask.request.form.get('delete') and (race := db.get_or_404(CharacterRace, flask.request.form.get('parentID'))):
            subraces = db.session.query(CharacterSubrace).filtter(CharacterSubrace.parent == race.id)
            characters = db.session.qury(Character).filter(Character.race == race.id)
            for c in characters:
                c.race = 21  # Human
                c.subrace = None
                db.session.add(c)

            _ = [db.session.delete(s) for s in subraces]

            db.session.delete(race)
        elif flask.request.form.get('name') and (race := CharacterRace(value=flask.request.form.get('name'))):
            db.session.add(race)

        db.session.commit()

    return render_template('/admin_pages/cat_admin/parent_list.html', parents=get_races(), parent_label="race",
                           child_label="subraces", href="admin.cat_admin.admin_subraces")

@cat_admin_blueprint.route('/races/<parent>', methods=['GET', 'POST'])
def admin_subraces(parent):
    db: SQLAlchemy = current_app.config.get('DB')
    parent = db.get_or_404(CharacterRace, parent)

    if flask.request.method == 'POST':
        if not flask.request.form.get('childID') and (subrace := CharacterSubrace(value=flask.request.form.get('name'), parent=parent.id)):
            db.session.add(subrace)
        elif subrace := db.get_or_404(CharacterSubrace, flask.request.form.get('childID')):
            if flask.request.form.get('update'):
                subrace.value = flask.request.form.get('childName')
                db.session.add(subrace)
            elif flask.request.form.get('delete'):
                db.session.delete(subrace)

        db.session.commit()

    return render_template('/admin_pages/cat_admin/child_list.html', children=get_subraces(parent.id),
                           parent_label="race", label="subrace", parent=parent,
                           parent_url="admin.cat_admin.admin_races")

