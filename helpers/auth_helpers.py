from functools import wraps

from flask import session, redirect, url_for, current_app, request
from sqlalchemy import and_

from models import User, Role


def is_admin(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_id = session.get('_user_id')
            if not user_id:
                return redirect(url_for('auth.login', next=request.endpoint))

            user = current_app.db.session.query(User).filter(and_(User.id == user_id, User.active == True)).first()

            role = current_app.db.session.query(Role).filter(Role.name == 'Admin').first()

            if not user.allowed([role.id]):
                return redirect(url_for('homepage'))
            return f(*args, **kwargs)
        return decorated_function


def is_chronicler(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = session.get('_user_id')
        if not user_id:
            return redirect(url_for('auth.login', next=request.endpoint))

        user = current_app.db.session.query(User).filter(and_(User.id == user_id, User.active == True)).first()

        admin_role = current_app.db.session.query(Role).filter(Role.name == 'Admin').first()
        press_role = current_app.db.session.query(Role).filter(Role.name == 'Press').first()

        if not user.allowed([admin_role.id, press_role.id]):
            return redirect(url_for('homepage'))
        return f(*args, **kwargs)

    return decorated_function
