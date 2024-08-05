from flask import Blueprint, render_template


adventures_blueprint = Blueprint("adventures", __name__)


@adventures_blueprint.route('/')
def adventure_list():
    return render_template('/adventures/adventures.html')
