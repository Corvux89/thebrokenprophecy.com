from flask import Blueprint, render_template


stats_blueprint = Blueprint("stats", __name__)

@stats_blueprint.route('/')
def census():
    return render_template('/stats/server_stats.html')