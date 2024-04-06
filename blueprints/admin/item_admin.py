import flask
from flask import Blueprint, render_template, current_app, url_for, redirect

from helpers import get_item_list, get_table_items, update_item, get_table, get_subtype
from helpers.admin_helpers import add_item
from models import Rarity, MagicSchool, CharacterClass

item_admin_blueprint = Blueprint("item_admin", __name__)
tables = ['Blacksmith', 'Consumable', 'Scroll', 'Wondrous']

@item_admin_blueprint.route('/items')
def item_list():
    return render_template('/admin_pages/item_admin/item_list.html', items=get_item_list())

@item_admin_blueprint.route('/items/<table>/<id>', methods=['GET', 'PATCH'])
def item_modify(table, id):
    if flask.request.method == 'PATCH':
        update_item(table, id, flask.request.form)
        return "complete"

    rarity = current_app.db.session.query(Rarity).all()
    item, sub_type, schools, classes = get_table_items(table, id)

    if not item or not table:
        return redirect(url_for("admin.item_admin.item_list"))

    return render_template('/admin_pages/item_admin/item_edit.html', item=item, table=table, subs=sub_type,
                           rarity=rarity, schools=schools, classes=classes)

@item_admin_blueprint.route('/items/add_item')
@item_admin_blueprint.route('/items/add_item/<table>', methods=['GET', 'POST'])
def item_new(table=None):
    if flask.request.method == 'POST':
        add_item(table, flask.request.form)

        return redirect(url_for("admin.item_admin.item_list"))

    if not table:
        return render_template('/admin_pages/item_admin/item_table.html', tables=tables)

    sub_type = get_subtype(table)
    rarity = current_app.db.session.query(Rarity).all()
    classes = current_app.db.session.query(CharacterClass).all() if table.lower() == 'scroll' else None
    schools = current_app.db.session.query(MagicSchool).all() if table.lower() == 'scroll' else None

    return render_template('/admin_pages/item_admin/item_add.html', table=table, subs=sub_type, rarity=rarity,
                           classes=classes, schools=schools)

@item_admin_blueprint.route('/items/<table>/<id>', methods=['DELETE'])
def item_delete(table, id):
    table = get_table(table)
    item = current_app.db.session.query(table).filter(table.id == id).first()

    if item is not None:
        current_app.db.session.delete(item)
        current_app.db.session.commit()

    return "complete"


