import json

from flask import Blueprint, render_template

factions_blueprint = Blueprint("factions", __name__)

@factions_blueprint.route('/')
def faction_list():
    f = open('json/factions.json', encoding="utf8")
    guild = json.load(f)
    return render_template('/factions/faction_list.html', guild=guild)