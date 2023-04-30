from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ARRAY

db = SQLAlchemy()


class Issue(db.Model):
    __tablename__ = 'chromatic_issues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    game_date = db.Column(db.String)
    publish_date = db.Column(db.DateTime)
    published = db.Column(db.Boolean)

    def get_date_formatted(self):
        return self.publish_date.strftime("%m/%d/%Y")

    def get_date(self):
        if self .publish_date is None:
            return None
        else:
            return self.publish_date.date()


class Author(db.Model):
    __tablename__ = "chromatic_authors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    title = db.Column(db.String)


class Article(db.Model):
    __tablename__ = "chromatic_articles"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    authors = db.Column(ARRAY(db.Integer))
    issue = db.Column(db.Integer)
    categories = db.Column(ARRAY(db.String))
    body = db.Column(db.String)
    players = db.Column(db.String)
    factions = db.Column(ARRAY(db.Integer))
    priority = db.Column(db.Integer)
    submit_user = db.Column(db.Integer)
    approved = db.Column(db.Boolean)
