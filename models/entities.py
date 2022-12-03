from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Character(db.Model):
    __tablename__ = 'characters'

    id = db.Column(db.Integer, primary_key=True)
    race = db.Column(db.Integer)
    subrace = db.Column(db.Integer)
    active = db.Column(db.Boolean)
    guild_id = db.Column(db.Integer)
    faction = db.Column(db.Integer)

class PlayerCharacterClass(db.Model):
    __tablename__ = 'character_class'

    id = db.Column(db.Integer, primary_key=True)
    character_id = db.Column(db.Integer)
    primary_class = db.Column(db.Integer)
    subclass = db.Column(db.Integer)
    active = db.Column(db.Boolean)