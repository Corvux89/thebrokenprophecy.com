import flask
from flask import Blueprint, current_app, render_template, redirect, url_for

from helpers import get_subclasses, get_classes, get_races
from models import CharacterClass, CharacterSubclass, PlayerCharacterClass, CharacterRace

cat_admin_blueprint = Blueprint("cat_admin", __name__)

# Character Classes and Subclasses
@cat_admin_blueprint.route('/classes', methods=['GET', 'POST'])
def admin_classes():
    if flask.request.method == 'POST':
        if flask.request.form.get('delete') and (c_class := current_app.db.get_or_404(CharacterClass, flask.request.form.get('parentID'))):
            subclasses = current_app.db.session.query(CharacterSubclass).filter(CharacterSubclass.parent == c_class.id)
            player_classes = current_app.db.session.query(PlayerCharacterClass).filter(PlayerCharacterClass.primary_class == c_class.id)
            for c in player_classes:
                c.primary_class = 13
                c.subclass = None
                current_app.db.session.add(c)

            for s in subclasses:
                current_app.db.session.delete(s)

            current_app.db.session.delete(c_class)
        elif flask.request.form.get('name') and (c_class := CharacterClass(value=flask.request.form.get('name'))):
            current_app.db.session.add(c_class)

        current_app.db.session.commit()

    return render_template('/admin_pages/cat_admin/parent_list.html', parents=get_classes(), parent_label="class",
                           child_label="subclass", href="admin.cat_admin.admin_subclasses")

@cat_admin_blueprint.route('/classes/<parent>', methods=['GET', 'POST'])
def admin_subclasses(parent):
    parent = current_app.db.get_or_404(CharacterClass, parent)

    if flask.request.method == 'POST':
        if not flask.request.form.get('childID') and (subclass := CharacterSubclass(value=flask.request.form.get('name'), parent=parent.id)):
            current_app.db.session.add(subclass)
        elif subclass := current_app.db.get_or_404(CharacterSubclass, flask.request.form.get('childID')):
            if flask.request.form.get('update'):
                subclass.value = flask.request.form.get('childName')
                current_app.db.session.add(subclass)
            elif flask.request.form.get('delete'):
                current_app.db.session.delete(subclass)

        current_app.db.session.commit()

    return render_template('/admin_pages/cat_admin/child_list.html', children=get_subclasses((parent.id)), parent_label="class", label="subclass",
                           path="classes", parent=parent, parent_url="admin.cat_admin.admin_classes")

# Character Races and Subraces
@cat_admin_blueprint.route('/races', methods=['GET', 'POST'])
def admin_races():
    if flask.request.method == 'POST':
        if flask.request.form.get('delete') and (race := current_app.db.get_or_404(CharacterRace, flask.request.form.get('parentID'))):
            return('here')
            # Do stuff here for delete
        elif flask.request.form.get('name') and (race := CharacterRace(value=flask.request.form.get('name'))):
            current_app.db.session.add(race)

        current_app.db.session.commit()

    return render_template('/admin_pages/cat_admin/parent_list.html', paren=get_races(), parent_label="race",
                           child_label="subraces", href="admin.cat_admin.admin_subraces")

