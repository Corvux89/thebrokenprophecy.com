import flask
from flask import Blueprint, current_app, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy

from blueprints.admin.category_admin import cat_admin_blueprint
from blueprints.admin.item_admin import item_admin_blueprint
from blueprints.admin.messages import message_blueprint
from constants import GUILD_ID
from helpers import is_admin, get_logs
from models import BPGuild

admin_blueprint = Blueprint("admin", __name__)
admin_blueprint.register_blueprint(cat_admin_blueprint)
admin_blueprint.register_blueprint(item_admin_blueprint)
admin_blueprint.register_blueprint(message_blueprint)

@admin_blueprint.before_request
@is_admin
def before_request():
    pass

@admin_blueprint.route('/')
def admin_menu():
    return render_template('/admin_pages/admin_menu.html')

@admin_blueprint.route('/greeting', methods=['GET', 'POST'])
def greeting_message():
    db: SQLAlchemy = current_app.config.get('DB')
    guild = db.get_or_404(BPGuild, GUILD_ID)

    if flask.request.method == 'POST':
        guild.greeting = flask.request.form.get('message')
        db.session.add(guild)
        db.session.commit()
        return redirect(f'{url_for("admin.admin_menu")}')


    return render_template('/admin_pages/admin_greeting_edit.html', guild=guild)

@admin_blueprint.route('/logs')
def view_logs():
    logs = get_logs()
    return render_template('/admin_pages/log_list.html', logs=logs)
