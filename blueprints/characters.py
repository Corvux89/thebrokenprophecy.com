from flask import Blueprint, render_template

from helpers import get_characters

characters_blueprint = Blueprint("characters", __name__)

@characters_blueprint.route('/')
def display_characters():
    characters = get_characters()
    return render_template('/characters/characters.html', characters=characters)