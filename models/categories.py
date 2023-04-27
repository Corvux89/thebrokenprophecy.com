from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class CharacterRace(db.Model):
    __tablename__ = 'c_character_race'

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String)
    pass

class CharacterSubrace(db.Model):
    __tablename__ = 'c_character_subrace'

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String)
    parent = db.Column(db.Integer)
    pass

class CharacterClass(db.Model):
    __tablename__ = 'c_character_class'

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String)
    pass

class CharacterSubclass(db.Model):
    __tablename__ = 'c_character_subclass'

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String)
    parent = db.Column(db.Integer)
    pass

class Rarity(db.Model):
    __tablename__ = 'c_rarity'

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String)

class BlackSmithType(db.Model):
    __tablename__ = 'c_blacksmith_type'

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String)

class ConsumableType(db.Model):
    __tablename__ = 'c_consumable_type'

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String)

class MagicSchool(db.Model):
    __tablename__ = 'c_magic_school'

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String)

class ChromaticCategory(db.Model):
    __tablename__ = "c_chromatic_categories"

    name = db.Column(db.String, primary_key=True)

class Faction(db.Model):
    __tablename__ = "c_faction"

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String)

class Activity(db.Model):
    __tablename__ = "c_activity"

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String)
    ratio = db.Column(db.Float)
    diversion = db.Column(db.Boolean)