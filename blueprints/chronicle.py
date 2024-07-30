from datetime import datetime

import flask
from flask import Blueprint, current_app, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_, desc

from helpers import is_chronicler, get_issues, get_articles, update_article, fetch_article, get_formatted_articles
from models import Article, Author, Issue, ChromaticCategory, Faction

chronicle_blueprint = Blueprint("chronicle", __name__)


@chronicle_blueprint.route('/')
@chronicle_blueprint.route('/<issue>')
def display_issue(issue=None):
    db: SQLAlchemy = current_app.config.get('DB')
    latest_issue = db.session.query(Issue).filter(Issue.published == True).order_by(
            desc(Issue.publish_date)).first()
    drop_string ="Previous Issues"

    if issue is not None:
        issue = db.session.query(Issue).filter(and_(Issue.id == issue, Issue.published == True)).first()
        if issue.id != latest_issue.id:
            drop_string="Other Issues"
    else:
        issue = latest_issue

    articles = get_formatted_articles(issue)
    issues = db.session.query(Issue).filter(and_(Issue.id != issue.id, Issue.published == True)).order_by(
        desc(Issue.publish_date)).all()

    return render_template('/chromatic_chronicle/display_issue.html', issue=issue, articles=articles, others=issues,
                           drop_string=drop_string)

@chronicle_blueprint.route('/<issue>/<article>')
def display_article(issue, article):
    db: SQLAlchemy = current_app.config.get('DB')
    issue = db.get_or_404(Issue, issue)
    article = db.get_or_404(Article, article)
    if not article.approved:
        return redirect(url_for('chronicle.display_issue', issue=issue.id))
    authors = db.session.query(Author).all()
    article.author_str = ', '.join([f"{a.name}" for a in authors if a.id in article.authors])
    return render_template('/chromatic_chronicle/display_article.html', issue=issue, article=article)


# Editor Stuff
@chronicle_blueprint.route('/editor')
@is_chronicler
def editor():
    issues = get_issues()
    return render_template('/chromatic_chronicle/edit_menu.html', issues=issues)


@chronicle_blueprint.route('/editor/<issue>')
@is_chronicler
def edit_issue(issue):
    db: SQLAlchemy = current_app.config.get('DB')
    issue = db.get_or_404(Issue, issue)
    articles = get_articles(issue.id)
    return render_template('/chromatic_chronicle/edit_issue.html', articles=articles, issue=issue)


@chronicle_blueprint.route('/editor/new_issue', methods=['POST'])
@is_chronicler
def new_issue():
    db: SQLAlchemy = current_app.config.get('DB')
    issue: Issue = Issue(
        name=flask.request.form.get('title'),
        game_date=flask.request.form.get('game-date')
    )

    db.session.add(issue)
    db.session.commit()

    return redirect(url_for('chronicle.editor'))


@chronicle_blueprint.route('/editor/<issue>/<article>', methods=['GET', 'POST'])
@is_chronicler
def edit_article(issue, article):
    db: SQLAlchemy = current_app.config.get('DB')

    if flask.request.method == 'POST':
        article = db.get_or_404(Article, article)
        article = update_article(article, flask.request)
        db.session.add(article)
        db.session.commit()
        return redirect(url_for("chronicle.edit_issue", issue=issue))

    article = db.get_or_404(Article, article)
    authors = db.session.query(Author).all()
    issue_max = db.session.query(Issue).order_by(Issue.id.desc()).first()
    categories = db.session.query(ChromaticCategory).all()
    factions = db.session.query(Faction).all()

    return render_template('/chromatic_chronicle/edit_article.html', article=article, issue=issue, authors=authors,
                           issue_max=issue_max.id, categories=categories, factions=factions)


@chronicle_blueprint.route('/editor/new_article/<issue>', methods=['POST', 'GET'])
@is_chronicler
def new_article(issue):
    db: SQLAlchemy = current_app.config.get('DB')

    if flask.request.method == 'POST':
        article = fetch_article(flask.request)
        db.session.add(article)
        db.session.commit()
        return redirect(url_for('chronicle.edit_issue', issue=issue))

    issue = db.get_or_404(Issue, issue)
    issue_max = db.session.query(Issue).order_by(Issue.id.desc()).first()
    authors = db.session.query(Author).all()
    categories = db.session.query(ChromaticCategory).all()
    factions = db.session.query(Faction).all()

    return render_template('/chromatic_chronicle/new_article.html', issue=issue, issue_max=issue_max, authors=authors,
                           categories=categories, factions=factions)


@chronicle_blueprint.route('/editor/delete_article/<article>', methods=['POST'])
@is_chronicler
def delete_article(article):
    db: SQLAlchemy = current_app.config.get('DB')

    article = db.get_or_404(Article, article)

    db.session.delete(article)
    db.session.commit()

    return redirect(url_for('chronicle.edit_issue', issue=article.issue))


@chronicle_blueprint.route('/editor/publish/<issue>/<pub>', methods=['GET'])
@is_chronicler
def publish_issue(issue, pub):
    db: SQLAlchemy = current_app.config.get('DB')

    issue = db.get_or_404(Issue, issue)
    if pub == "True":
        issue.published = True
        issue.publish_date = datetime.utcnow()
        db.session.add(issue)
        db.session.commit()

    elif pub == "False":
        issue.published = False
        issue.publish_date = None

        db.session.add(issue)
        db.session.commit()

    return redirect(url_for('chronicle.edit_issue', issue=issue.id))


@chronicle_blueprint.route('/editor/edit/<issue>', methods=['POST'])
@is_chronicler
def modify_issue(issue):
    db: SQLAlchemy = current_app.config.get('DB')
    issue = db.get_or_404(Issue, issue)

    issue.name = flask.request.form.get('title')
    issue.game_date = "" if flask.request.form.get('game-date') is None else flask.request.form.get('game-date')
    issue.publish_date = None if flask.request.form.get('publish-date') is None else datetime.strptime(
        flask.request.form.get('publish-date'), "%Y-%m-%d")

    db.session.add(issue)
    db.session.commit()

    return redirect(url_for('chronicle.edit_issue', issue=issue.id))


@chronicle_blueprint.route('/editor/edit_author/<action>', methods=['POST'])
@is_chronicler
def edit_author(action):
    db: SQLAlchemy = current_app.config.get('DB')

    if action == "new":
        author: Author = Author(
            name=flask.request.form.get('naName'),
            title=None if flask.request.form.get('naTitle') is None else flask.request.form.get('naTitle')
        )

        db.session.add(author)
        db.session.commit()


    elif action == "update":
        id = flask.request.form.get('authorID')

        if id is not None:
            author = db.get_or_404(Author, id)

            if flask.request.form.get('submit') is not None:
                author.name = flask.request.form.get('authorName')
                author.title = None if flask.request.form.get('authorTitle') is None else flask.request.form.get(
                    'authorTitle')

                db.session.add(author)
                db.session.commit()
            elif flask.request.form.get('delete') is not None:
                db.session.delete(author)
                db.session.commit()

    return redirect(url_for('chronicle.view_authors'))


@chronicle_blueprint.route('/editor/authors', methods=['GET', 'POST'])
@is_chronicler
def view_authors():
    db: SQLAlchemy = current_app.config.get('DB')

    authors = db.session.query(Author).all()

    return render_template('/chromatic_chronicle/edit_author.html', authors=authors)

@chronicle_blueprint.route('/editor/<issue>/<article>/approve/<approve>')
@is_chronicler
def approve_article(issue, article, approve):
    db: SQLAlchemy = current_app.config.get('DB')
    article = db.get_or_404(Article,article)
    article.approved = False if approve=="False" else True
    db.session.add(article)
    db.session.commit()

    authors = db.session.query(Author).all()
    issue_max = db.session.query(Issue).order_by(Issue.id.desc()).first()
    categories = db.session.query(ChromaticCategory).all()
    factions = db.session.query(Faction).all()

    return render_template('/chromatic_chronicle/edit_article.html', issue=issue, article=article, authors=authors,
                           issue_max=issue_max.id, categories=categories, factions=factions)
