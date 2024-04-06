import flask
from flask import Blueprint, current_app, render_template, Response

from helpers import get_subclasses, get_classes, get_races, get_subraces
from models import CharacterClass, CharacterSubclass, PlayerCharacterClass, CharacterRace, CharacterSubrace, Character, \
    ScrollItem

# cat_admin_blueprint = Blueprint("cat_admin", __name__)

# Character Races and Subraces
# @cat_admin_blueprint.route('/races', methods=['GET', 'POST'])
# def admin_races():
#     if flask.request.method == 'POST':
#         if flask.request.form.get('delete') and (race := current_app.db.get_or_404(CharacterRace, flask.request.form.get('parentID'))):
#             subraces = current_app.db.session.query(CharacterSubrace).filtter(CharacterSubrace.parent == race.id)
#             characters = current_app.db.session.qury(Character).filter(Character.race == race.id)
#             for c in characters:
#                 c.race = 21  # Human
#                 c.subrace = None
#                 current_app.db.session.add(c)
#
#             _ = [current_app.db.session.delete(s) for s in subraces]
#
#             current_app.db.session.delete(race)
#         elif flask.request.form.get('name') and (race := CharacterRace(value=flask.request.form.get('name'))):
#             current_app.db.session.add(race)
#
#         current_app.db.session.commit()
#
#     return render_template('/admin_pages/cat_admin/parent_list.html', parents=get_races(), parent_label="race",
#                            child_label="subraces", href="admin.cat_admin.admin_subraces")
#
# @cat_admin_blueprint.route('/races/<id>', methods=['DELETE'])
# def delete_race(id):
#     if race := current_app.db.get_or_404(CharacterRace, id):
#         subraces = current_app.db.session.query(CharacterSubrace).filtter(CharacterSubrace.parent == race.id)
#         characters = current_app.db.session.qury(Character).filter(Character.race == race.id)
#         for c in characters:
#             c.race = 21  # Human
#             c.subrace = None
#             current_app.db.session.add(c)
#
#         _ = [current_app.db.session.delete(s) for s in subraces]
#
#         current_app.db.session.delete(race)
#         current_app.db.session.commit()
#
#         return "complete"
#     return Response(json.dumps())
#
# @cat_admin_blueprint.route('/races/<parent>', methods=['GET', 'POST'])
# def admin_subraces(parent):
#     parent = current_app.db.get_or_404(CharacterRace, parent)
#
#     if flask.request.method == 'POST':
#         if not flask.request.form.get('childID') and (subrace := CharacterSubrace(value=flask.request.form.get('name'), parent=parent.id)):
#             current_app.db.session.add(subrace)
#         elif subrace := current_app.db.get_or_404(CharacterSubrace, flask.request.form.get('childID')):
#             if flask.request.form.get('update'):
#                 subrace.value = flask.request.form.get('childName')
#                 current_app.db.session.add(subrace)
#             elif flask.request.form.get('delete'):
#                 current_app.db.session.delete(subrace)
#
#         current_app.db.session.commit()
#
#     return render_template('/admin_pages/cat_admin/child_list.html', children=get_subraces(parent.id),
#                            parent_label="race", label="subrace", parent=parent,
#                            parent_url="admin.cat_admin.admin_races")

