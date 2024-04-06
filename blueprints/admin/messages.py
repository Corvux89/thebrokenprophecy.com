import flask
from flask import Blueprint, current_app, render_template, redirect, url_for

from constants import GUILD_ID
from helpers import get_messages
from models import BPMessage

message_blueprint = Blueprint("message", __name__)


@message_blueprint.route('/message', methods=['GET', 'POST'])
def new_message():
    channels = current_app.discord.bot_request(f'/guilds/{GUILD_ID}/channels')
    if flask.request.method == 'POST':
        msg = current_app.discord.bot_request(f'/channels/{flask.request.form.get("channel")}/messages', 'POST',
                                              json={"content": flask.request.form.get("message")})
        if msg.get('id'):
            if flask.request.form.get('pin'):
                current_app.discord.bot_request(f'/channels/{flask.request.form.get("channel")}/pins/{msg.get("id")}',
                                                'PUT')

            bpm = BPMessage(guild_id=GUILD_ID, message_id=msg.get('id'),
                            channel_id=flask.request.form.get("channel"),
                            title=flask.request.form.get("title"))
            current_app.db.session.add(bpm)
            current_app.db.session.commit()

        return redirect(url_for('admin.message.new_message'))

    messages = get_messages()

    return render_template('/admin_pages/messages/message.html', channels=channels, msgs=messages)


@message_blueprint.route('/message/<id>', methods=['DELETE'])
def delete_message(id):
    bpm = current_app.db.get_or_404(BPMessage, id)
    current_app.discord.bot_request(f'/channels/{bpm.channel_id}/messages/{id}', 'DELETE')
    current_app.db.session.delete(bpm)
    current_app.db.session.commit()

    return "deleted"


@message_blueprint.route('/message/<id>', methods=['PATCH'])
def edit_message(id):
    bpm = current_app.db.get_or_404(BPMessage, id)

    msg = current_app.discord.bot_request(f'/channels/{bpm.channel_id}/messages/{id}', 'PATCH',
                                          json={"content": flask.request.form.get(f"edit-{id}-message")})

    if bool(msg.get('pinned', False)) != bool(flask.request.form.get(f"edit-{id}-pin", False)):
        if flask.request.form.get(f"edit-{id}-pin"):
            current_app.discord.bot_request(f'/channels/{bpm.channel_id}/pins/{id}', 'PUT')
        else:
            current_app.discord.bot_request(f'/channels/{bpm.channel_id}/pins/{id}', 'DELETE')

    if bpm.title != flask.request.form.get(f'edit-{id}-title'):
        bpm.title = flask.request.form.get(f'edit-{id}-title')
        current_app.db.session.add(bpm)
        current_app.db.session.commit()

    return "edited"
