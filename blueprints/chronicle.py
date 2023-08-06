from datetime import datetime

import flask
from flask import Blueprint, current_app, redirect, url_for, render_template
from sqlalchemy import and_, desc

from helpers import is_chronicler, get_issues, get_articles, update_article, fetch_article, get_formatted_articles
from models import Article, Author, Issue, ChromaticCategory, Faction

chronicle_blueprint = Blueprint("chronicle", __name__)


@chronicle_blueprint.route('/')
@chronicle_blueprint.route('/<issue>')
def display_issue(issue=None):
    latest_issue = current_app.db.session.query(Issue).filter(Issue.published == True).order_by(
            desc(Issue.publish_date)).first()
    drop_string ="Previous Issues"

    if issue is not None:
        issue = current_app.db.session.query(Issue).filter(and_(Issue.id == issue, Issue.published == True)).first()
        if issue.id != latest_issue.id:
            drop_string="Other Issues"
    else:
        issue = latest_issue

    articles = get_formatted_articles(issue)
    issues = current_app.db.session.query(Issue).filter(and_(Issue.id != issue.id, Issue.published == True)).order_by(
        desc(Issue.publish_date)).all()

    return render_template('/chromatic_chronicle/display_issue1.html', issue=issue, articles=articles, others=issues,
                           drop_string=drop_string)

@chronicle_blueprint.route('/<issue>/<article>')
def display_article(issue, article):
    issue = current_app.db.get_or_404(Issue, issue)
    article = current_app.db.get_or_404(Article, article)
    if not article.approved:
        return redirect(url_for('chronicle.display_issue', issue=issue.id))
    authors = current_app.db.session.query(Author).all()
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
    issue = current_app.db.get_or_404(Issue, issue)
    articles = get_articles(issue.id)
    return render_template('/chromatic_chronicle/edit_issue.html', articles=articles, issue=issue)


@chronicle_blueprint.route('/editor/new_issue', methods=['POST'])
@is_chronicler
def new_issue():
    issue: Issue = Issue(
        name=flask.request.form.get('title'),
        game_date=flask.request.form.get('game-date')
    )

    current_app.db.session.add(issue)
    current_app.db.session.commit()

    return redirect(url_for('chronicle.editor'))


@chronicle_blueprint.route('/editor/<issue>/<article>', methods=['GET', 'POST'])
@is_chronicler
def edit_article(issue, article):
    if flask.request.method == 'POST':
        article = current_app.db.get_or_404(Article, article)
        article = update_article(article, flask.request)
        current_app.db.session.add(article)
        current_app.db.session.commit()
        return redirect(url_for("chronicle.edit_issue", issue=issue))

    article = current_app.db.get_or_404(Article, article)
    authors = current_app.db.session.query(Author).all()
    issue_max = current_app.db.session.query(Issue).order_by(Issue.id.desc()).first()
    categories = current_app.db.session.query(ChromaticCategory).all()
    factions = current_app.db.session.query(Faction).all()

    return render_template('/chromatic_chronicle/edit_article.html', article=article, issue=issue, authors=authors,
                           issue_max=issue_max.id, categories=categories, factions=factions)


@chronicle_blueprint.route('/editor/new_article/<issue>', methods=['POST', 'GET'])
@is_chronicler
def new_article(issue):
    if flask.request.method == 'POST':
        article = fetch_article(flask.request)
        current_app.db.session.add(article)
        current_app.db.session.commit()
        return redirect(url_for('chronicle.edit_issue', issue=issue))

    issue = current_app.db.get_or_404(Issue, issue)
    issue_max = current_app.db.session.query(Issue).order_by(Issue.id.desc()).first()
    authors = current_app.db.session.query(Author).all()
    categories = current_app.db.session.query(ChromaticCategory).all()
    factions = current_app.db.session.query(Faction).all()

    return render_template('/chromatic_chronicle/new_article.html', issue=issue, issue_max=issue_max, authors=authors,
                           categories=categories, factions=factions)


@chronicle_blueprint.route('/editor/delete_article/<article>', methods=['POST'])
@is_chronicler
def delete_article(article):
    article = current_app.db.get_or_404(Article, article)

    current_app.db.session.delete(article)
    current_app.db.session.commit()

    return redirect(url_for('chronicle.edit_issue', issue=article.issue))


@chronicle_blueprint.route('/editor/publish/<issue>/<pub>', methods=['GET'])
@is_chronicler
def publish_issue(issue, pub):
    issue = current_app.db.get_or_404(Issue, issue)
    if pub == "True":
        issue.published = True
        issue.publish_date = datetime.utcnow()
        current_app.db.session.add(issue)
        current_app.db.session.commit()

    elif pub == "False":
        issue.published = False
        issue.publish_date = None

        current_app.db.session.add(issue)
        current_app.db.session.commit()

    return redirect(url_for('chronicle.edit_issue', issue=issue.id))


@chronicle_blueprint.route('/editor/edit/<issue>', methods=['POST'])
@is_chronicler
def modify_issue(issue):
    issue = current_app.db.get_or_404(Issue, issue)

    issue.name = flask.request.form.get('title')
    issue.game_date = "" if flask.request.form.get('game-date') is None else flask.request.form.get('game-date')
    issue.publish_date = None if flask.request.form.get('publish-date') is None else datetime.strptime(
        flask.request.form.get('publish-date'), "%Y-%m-%d")

    current_app.db.session.add(issue)
    current_app.db.session.commit()

    return redirect(url_for('chronicle.edit_issue', issue=issue.id))


@chronicle_blueprint.route('/editor/edit_author/<action>', methods=['POST'])
@is_chronicler
def edit_author(action):
    if action == "new":
        author: Author = Author(
            name=flask.request.form.get('naName'),
            title=None if flask.request.form.get('naTitle') is None else flask.request.form.get('naTitle')
        )

        current_app.db.session.add(author)
        current_app.db.session.commit()


    elif action == "update":
        id = flask.request.form.get('authorID')

        if id is not None:
            author = current_app.db.get_or_404(Author, id)

            if flask.request.form.get('submit') is not None:
                author.name = flask.request.form.get('authorName')
                author.title = None if flask.request.form.get('authorTitle') is None else flask.request.form.get(
                    'authorTitle')

                current_app.db.session.add(author)
                current_app.db.session.commit()
            elif flask.request.form.get('delete') is not None:
                current_app.db.session.delete(author)
                current_app.db.session.commit()

    return redirect(url_for('chronicle.view_authors'))


@chronicle_blueprint.route('/editor/authors', methods=['GET', 'POST'])
@is_chronicler
def view_authors():
    authors = current_app.db.session.query(Author).all()

    return render_template('/chromatic_chronicle/edit_author.html', authors=authors)

@chronicle_blueprint.route('/editor/<issue>/<article>/approve/<approve>')
@is_chronicler
def approve_article(issue, article, approve):
    article = current_app.db.get_or_404(Article,article)
    article.approved = False if approve=="False" else True
    current_app.db.session.add(article)
    current_app.db.session.commit()

    return render_template('/chromatic_chronicle/edit_article.html', issue=issue, article=article)
