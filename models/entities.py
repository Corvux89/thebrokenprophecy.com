import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import DateTime, Integer

db = SQLAlchemy()

class Character(db.Model):
    __tablename__ = 'characters'
    id: Mapped[int] = mapped_column(primary_key=True)
    player_id: Mapped[int]
    name: Mapped[str]
    race: Mapped[int]
    subrace: Mapped[int]
    active: Mapped[bool]
    guild_id: Mapped[int]
    xp: Mapped[int]
    

class PlayerCharacterClass(db.Model):
    __tablename__ = 'character_class'
    id: Mapped[int] = mapped_column(primary_key=True)
    character_id: Mapped[int]
    primary_class: Mapped[int]
    subclass: Mapped[int]
    active: Mapped[bool]

class BlackSmithItem(db.Model):
    __tablename__ = 'item_blacksmith'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    sub_type: Mapped[int]
    rarity: Mapped[int]
    cost: Mapped[int]
    item_modifier: Mapped[bool]
    attunement: Mapped[bool]
    seeking_only: Mapped[bool]
    source: Mapped[str]
    notes: Mapped[str]


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