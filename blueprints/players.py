from flask import Blueprint, render_template

from helpers import get_players

players_blueprint = Blueprint("players", __name__)

@players_blueprint.route('/')
def display_players():
    players = get_players()
    return render_template('players.html', players=players)
