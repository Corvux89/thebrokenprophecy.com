from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import ARRAY

db = SQLAlchemy()

class Character(db.Model):
    __tablename__ = 'characters'

    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer)
    name = db.Column(db.String)
    race = db.Column(db.Integer)
    subrace = db.Column(db.Integer)
    active = db.Column(db.Boolean)
    guild_id = db.Column(db.Integer)

class PlayerCharacterClass(db.Model):
    __tablename__ = 'character_class'

    id = db.Column(db.Integer, primary_key=True)
    character_id = db.Column(db.Integer)
    primary_class = db.Column(db.Integer)
    subclass = db.Column(db.Integer)
    active = db.Column(db.Boolean)


class BlackSmithItem(db.Model):
    __tablename__ = 'item_blacksmith'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    sub_type = db.Column(db.Integer)
    rarity = db.Column(db.Integer)
    cost = db.Column(db.Integer)
    item_modifier = db.Column(db.Boolean)
    attunement = db.Column(db.Boolean)
    seeking_only = db.Column(db.Boolean)
    source = db.Column(db.String)
    notes = db.Column(db.String)

class ConsumableItem(db.Model):
    __tablename__ = 'item_consumable'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    sub_type = db.Column(db.Integer)
    rarity = db.Column(db.Integer)
    cost = db.Column(db.Integer)
    attunement = db.Column(db.Boolean)
    seeking_only = db.Column(db.Boolean)
    source = db.Column(db.String)
    notes = db.Column(db.String)


class ScrollItem(db.Model):
    __tablename__ = 'item_scrolls'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    rarity = db.Column(db.Integer)
    cost = db.Column(db.Integer)
    level = db.Column(db.Integer)
    school = db.Column(db.Integer)
    classes = db.Column(ARRAY(db.Integer))
    source = db.Column(db.String)
    notes = db.Column(db.String)

class WondrousItem(db.Model):
    __tablename__ = 'item_wondrous'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    rarity = db.Column(db.Integer)
    cost = db.Column(db.Integer)
    attunement = db.Column(db.Boolean)
    seeking_only = db.Column(db.Boolean)
    source = db.Column(db.String)
    notes = db.Column(db.String)

class Adventures(db.Model):
    __tablename__ = 'adventures'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    role_id = db.Column(db.Integer)
    dms = db.Column(ARRAY(db.Integer))
    tier = db.Column(db.Integer)
    ep = db.Column(db.Integer)
    end_ts = db.Column(db.DateTime)
    guild_id = db.Column(db.Integer)