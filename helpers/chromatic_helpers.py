import calendar

import flask
from flask import current_app
from sqlalchemy import func, and_

from models import *


def get_issues():
    issues = current_app.db.session.query(Issue).all()

    art_count = current_app.db.session.query(Issue.id, func.count(Article.issue).label('count')) \
        .join(Article, Article.issue == Issue.id) \
        .group_by(Issue.id).all()

    approved_count = current_app.db.session.query(Issue.id, func.count(Article.issue).label('count'))\
        .join(Article, Article.issue == Issue.id) \
        .filter(Article.approved == True)\
        .group_by(Issue.id).all()

    d_out = []

    for i in issues:

        i_dict = {'id': i.id, 'name': i.name, 'published': 'Yes' if i.published else 'No',
                  'publish_date': "" if i.publish_date is None else i.get_date_formatted(), 'articles': 0}

        for c in art_count:
            if c.id == i.id:
                for a in approved_count:
                    if a.id == c.id:
                        i_dict['articles'] = f"{a.count} ({c.count})"
                        break
        d_out.append(i_dict)

    d_out = sorted(d_out, key=lambda i: i['id'], reverse=True)

    return d_out


def get_articles(issue):
    articles = current_app.db.session.query(Article).filter(Article.issue == issue).all()
    authors = current_app.db.session.query(Author).all()

    d_out = []

    for a in articles:
        a_dict = {'id': a.id, 'title': a.title, 'priority': a.priority, 'author_list': [],
                  'categories': ", ".join(f"{c}" for c in a.categories), 'approved': a.approved}

        for a in a.authors:
            for author in authors:
                if author.id == a:
                    a_dict['author_list'].append(author)
                    break

        a_dict['authors'] = ", ".join(f"{a.name}" for a in a_dict['author_list'])
        d_out.append(a_dict)

    return d_out


def update_article(article: Article, request: flask.Request):
    article.title = request.form.get('title')
    article.issue = request.form.get('issue')
    article.authors = request.form.getlist('authors')
    article.players = None if request.form.get('players') == "None" else request.form.get('players')
    article.priority = request.form.get('priority')
    article.body = request.form.get('body')
    article.categories = request.form.getlist('categories')

    factions = [f[1] for f in request.form.items() if 'faction' in f[0]]

    article.factions = factions

    return article


def fetch_article(request: flask.Request):
    article: Article = Article(
        title=request.form.get('title'),
        issue=request.form.get('issue'),
        authors=request.form.getlist('authors'),
        players=None if request.form.get('players') == "None" else request.form.get('players'),
        priority=request.form.get('priority'),
        body=request.form.get('body'),
        categories=request.form.getlist('categories'),
        approved=False,
        submit_user=current_app.discord.fetch_user().id
    )

    factions = [f for f in request.form.items() if 'faction' in f[0]]

    article.factions = factions

    return article


def get_formatted_articles(issue: Issue):
    articles = current_app.db.session.query(Article).filter(and_(Article.issue == issue.id, Article.approved==True)).all()
    authors = current_app.db.session.query(Author).all()
    factions = current_app.db.session.query(Faction).all()

    for a in articles:
        a.faction_list = [f for f in factions if f.id in a.factions]
        a.faction_string = ", ".join(f"{f.value}" for f in a.faction_list)
        a.author_list = [auth for auth in authors if auth.id in a.authors]

        a.author_string = ", ".join(f"{c.name} - <i>{c.title}</i>" for c in a.author_list)
        a.category_string = ", ".join(f"#{c}" for c in a.categories)

        if "global" in a.category_string:
            a.preview = ' '.join(a.body.split()[:75]) + "..."
        else:
            a.preview = ' '.join(a.body.split()[:25]) + "..."

    articles = sorted(articles, key=lambda x: (x.priority, x.title))

    return articles
