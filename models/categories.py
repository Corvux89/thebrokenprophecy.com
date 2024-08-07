from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import mapped_column, Mapped

db = SQLAlchemy()

class CharacterRace(db.Model):
    __tablename__ = 'c_character_race'
    id: Mapped[int] = mapped_column(primary_key=True)
    value: Mapped[str]
    
class CharacterSubrace(db.Model):
    __tablename__ = 'c_character_subrace'
    id: Mapped[int] = mapped_column(primary_key=True)
    value: Mapped[str]
    parent: Mapped[int]

class CharacterClass(db.Model):
    __tablename__ = 'c_character_class'
    id: Mapped[int] = mapped_column(primary_key=True)
    value: Mapped[str]

class CharacterSubclass(db.Model):
    __tablename__ = 'c_character_subclass'
    id: Mapped[int] = mapped_column(primary_key=True)
    value: Mapped[str]
    parent: Mapped[int]

class Rarity(db.Model):
    __tablename__ = 'c_rarity'
    id: Mapped[int] = mapped_column(primary_key=True)
    value: Mapped[str]

class BlackSmithType(db.Model):
    __tablename__ = 'c_blacksmith_type'
    id: Mapped[int] = mapped_column(primary_key=True)
    value: Mapped[str]

class ConsumableType(db.Model):
    __tablename__ = 'c_consumable_type'
    id: Mapped[int] = mapped_column(primary_key=True)
    value: Mapped[str]

class MagicSchool(db.Model):
    __tablename__ = 'c_magic_school'
    id: Mapped[int] = mapped_column(primary_key=True)
    value: Mapped[str]

class ChromaticCategory(db.Model):
    __tablename__ = "c_chromatic_categories"

    name = db.Column(db.String, primary_key=True)

class Faction(db.Model):
    __tablename__ = "c_faction"
    id: Mapped[int] = mapped_column(primary_key=True)
    value: Mapped[str]

class Activity(db.Model):
    __tablename__ = "c_activity"

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String)
    ratio = db.Column(db.Float)
    diversion = db.Column(db.Boolean)