import functools

import flask

from werkzeug.security import generate_password_hash, check_password_hash
from .db import get_db

auth_bp = flask.Blueprint('auth', __name__, url_prefix='/auth')


def login_required(allowed_role=None):
    def wrapper(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            if flask.g.user is None or (allowed_role and flask.session.get('role') not in allowed_role):
                return flask.redirect(flask.url_for('auth.login'))
            return func(*args, **kwargs)
        return inner
    return wrapper


@auth_bp.route('/', endpoint='register', methods=('GET', 'POST'))
def register():
    if flask.request.method == 'GET':
        return flask.render_template('register.html')
    else:
        username = flask.request.form['username']
        password = flask.request.form['password']

        db = get_db()

        error = None

        if not username:
            error = 'Username is required'
        elif not password:
            error = 'Password is required'
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username, )
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            db.execute(
                "INSERT INTO user (username, password) VALUES (?, ?)",
                (username, generate_password_hash(password))
            )
            db.commit()
            flask.flash('Registered successfully! Try logging-in now!', 'success')
            return flask.redirect(flask.url_for('auth.login'))

        flask.flash(error, category='error')
        return flask.render_template('register.html')


@auth_bp.route('/login/', endpoint='login', methods=('GET', 'POST'))
def login():
    if flask.request.method == 'GET':
        return flask.render_template('login.html')
    else:
        username = flask.request.form['username']
        password = flask.request.form['password']

        db = get_db()
        error = None
        user = None

        if not username:
            error = 'Username is required'
        elif not password:
            error = 'Password is required'
        else:
            user = db.execute(
                'SELECT * FROM user WHERE username = ?', (username,)
            ).fetchone()

            if not user or not check_password_hash(user['password'], password):
                error = 'Username or password is incorrect'

        if error is None:
            flask.session.clear()
            flask.session['user_id'] = user['id']
            return flask.redirect(flask.url_for('views.home'))

        flask.flash(error, category='error')

        return flask.render_template('login.html')


@auth_bp.route('/logout', endpoint='logout')
def logout():
    flask.session.clear()
    return flask.redirect(flask.url_for('index'))


@auth_bp.before_app_request
def load_logged_in_user():
    user_id = flask.session.get('user_id')

    if user_id is None:
        flask.g.user = None
    else:
        db = get_db()
        flask.g.user = db.execute(
            'SELECT * from user where id = ?', (user_id, )
        ).fetchone()
