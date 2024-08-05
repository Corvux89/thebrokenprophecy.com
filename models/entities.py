import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import DateTime, Integer

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
    xp = db.Column(db.Integer)

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
    notes = db.Column(db.String, default=None)

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

class Adventure(db.Model):
    __tablename__ = 'adventures'
    id: Mapped[int] = mapped_column(primary_key = True)
    name: Mapped[str]
    role_id: Mapped[int]
    dms: Mapped[list[int]] = mapped_column(ARRAY(Integer))
    tier: Mapped[int]
    ep: Mapped[int]
    end_ts: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True))
    guild_id: Mapped[int]

class BPLog(db.Model):
    __tablename__ = 'log'

    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.Integer)
    xp = db.Column(db.Integer)
    server_xp = db.Column(db.Integer)
    gold = db.Column(db.Integer)
    created_ts = db.Column(db.DateTime)
    character_id = db.Column(db.Integer)
    activity = db.Column(db.Integer)
    notes = db.Column(db.String)
    shop_id = db.Column(db.Integer)
    adventure_id = db.Column(db.Integer)
    invalid = db.Column(db.Boolean)

class BPGuild(db.Model):
    __tablename__ = 'guilds'

    id = db.Column(db.Integer, primary_key=True)
    greeting = db.Column(db.String)

class BPMessage(db.Model):
    __tablename__ = "messages"

    message_id = db.Column(db.Integer, primary_key=True)
    guild_id = db.Column(db.Integer)
    channel_id = db.Column(db.Integer)
    title = db.Column(db.String)