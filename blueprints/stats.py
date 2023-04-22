from flask import Blueprint, render_template

from helpers import get_race_table, get_class_table

stats_blueprint = Blueprint("stats", __name__)

@stats_blueprint.route('/')
def census():
    race_data = get_race_table()
    class_data = get_class_table()

    return render_template('/stats/server_stats.html', race_data=race_data, class_data=class_data)