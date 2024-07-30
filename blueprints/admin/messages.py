import flask
from flask import Blueprint, current_app, render_template, redirect, url_for
from flask_discord import DiscordOAuth2Session
from flask_sqlalchemy import SQLAlchemy

from constants import GUILD_ID
from helpers import get_messages
from models import BPMessage

message_blueprint = Blueprint("message", __name__)

@message_blueprint.route('/message', methods=['GET', 'POST'])
def new_message():
    discord_session: DiscordOAuth2Session = current_app.config.get('DISCORD_SESSION')
    channels = discord_session.bot_request(f'/guilds/{GUILD_ID}/channels')

    if flask.request.method == 'POST':
        db: SQLAlchemy = current_app.config.get('DB')
        if flask.request.form.get('send'):
            msg = current_app.discord.bot_request(f'/channels/{flask.request.form.get("channel")}/messages', 'POST',
                                                  json={"content": flask.request.form.get("message")})
            if msg.get('id'):
                if flask.request.form.get('pin'):
                    current_app.discord.bot_request(f'/channels/{flask.request.form.get("channel")}/pins/{msg.get("id")}', 'PUT')

                bpm = BPMessage(guild_id=GUILD_ID, message_id=msg.get('id'),
                                                     channel_id=flask.request.form.get("channel"),
                                                     title=flask.request.form.get("title"))
                db.session.add(bpm)
                db.session.commit()
        elif flask.request.form.get('edit'):
            msg_id = flask.request.args.get('msg')
            bpm = db.get_or_404(BPMessage, msg_id)

            msg = current_app.discord.bot_request(f'/channels/{bpm.channel_id}/messages/{msg_id}', 'PATCH',
                                                  json={"content": flask.request.form.get(f"edit-{msg_id}-message")})

            if bool(msg.get('pinned', False)) != bool(flask.request.form.get(f"edit-{msg_id}-pin",False)):
                if flask.request.form.get(f"edit-{msg_id}-pin"):
                    current_app.discord.bot_request(f'/channels/{bpm.channel_id}/pins/{msg_id}', 'PUT')
                else:
                    current_app.discord.bot_request(f'/channels/{bpm.channel_id}/pins/{msg_id}', 'DELETE')

            if bpm.title != flask.request.form.get(f'edit-{msg_id}-title'):
                bpm.title = flask.request.form.get(f'edit-{msg_id}-title')
                db.session.add(bpm)
                db.session.commit()
        elif flask.request.form.get('delete'):
            msg_id = flask.request.args.get('msg')
            bpm = db.get_or_404(BPMessage, msg_id)

            current_app.discord.bot_request(f'/channels/{bpm.channel_id}/messages/{msg_id}', 'DELETE')
            db.session.delete(bpm)
            db.session.commit()


        return redirect(url_for('admin.message.new_message'))

    messages = get_messages()

    return render_template('/admin_pages/messages/message.html', channels=channels, msgs=messages)

