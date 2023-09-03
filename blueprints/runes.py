import json

import flask
from flask import Blueprint, render_template, url_for, current_app, session

runes_blueprint = Blueprint("rune", __name__)

@runes_blueprint.route('/')
def runes():
    f = open('json/rune.json', encoding="utf8")
    info = json.load(f)
    total_url = url_for('rune.total')
    return render_template('/runes/runes.html', info=info, total_url=total_url)

@runes_blueprint.route('/total', methods=['POST'])
def total():
    form = flask.request.json
    f = open('json/rune.json', encoding="utf8")
    info = json.load(f)
    sum = 0
    cost = 0

    for field in form:
        if field in [n["name"] for n in info["runes"]]:
            rune = next((x for x in info["runes"] if x["name"] == field),None)
            value = int(form[field]) if form[field] else 0
            adj = float(rune.get("point",0))
            sum += value * adj
            cost += int(rune.get("cost",0))*value
    output = {
        "total": f"{str(int(sum) if sum % 1 ==0 else sum)}",
        "cost": f"{str(int(cost))}"
    }
    return output