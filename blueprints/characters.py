from flask import Blueprint, render_template


characters_blueprint = Blueprint("characters", __name__)

@characters_blueprint.route('/')
def display_characters():
    return render_template('/characters/characters.html')
