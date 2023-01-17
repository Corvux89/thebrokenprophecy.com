from functools import wraps

from flask import url_for, redirect, session, current_app
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ARRAY, and_

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    active = db.Column(db.Boolean)
    roles = db.Column(ARRAY(db.Integer))

    def allowed(self, roles):
        return any(r in roles for r in self.roles)
class Role(db.Model):
    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)


def has_role(roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not session.get('user_id'):
                return redirect(url_for('admin.admin_base'))

            user = current_app.db.get_or_404(User, session['user_id'])

            role_check = []

            for r in roles:
                r_obj = current_app.db.session.query(Role).filter(Role.name == r).first()
                role_check.append(r_obj.id)

            if not user.allowed(role_check):
                return redirect(url_for('homepage'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def is_admin(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_id = session.get('_user_id')
            if not user_id:
                return redirect(url_for('admin.admin_base'))

            user = current_app.db.session.query(User).filter(and_(User.id == user_id, User.active == True)).first()

            role = current_app.db.session.query(Role).filter(Role.name == 'Admin').first()

            if not user.allowed([role.id]):
                return redirect(url_for('homepage'))
            return f(*args, **kwargs)
        return decorated_function


