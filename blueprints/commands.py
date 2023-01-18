import json

from flask import Blueprint, render_template

commands_blueprint = Blueprint("commands", __name__)

@commands_blueprint.route('/')
def command_list():
    f = open('json/commands.json')
    commands = json.load(f)
    return render_template('commands.html', commands=commands['category'], role_list=commands['roles'])

@commands_blueprint.route('/<role>')
def role_commands(role):
    f = open('json/commands.json')
    commands = json.load(f)
    filter_commands = {}
    filter_commands['category'] = []

    for c in commands['category']:
        if "role" in c and role in c["role"]:
            filter_commands['category'].append(c)

    return render_template('commands.html', commands=filter_commands['category'], role=role, role_list=commands['roles'])