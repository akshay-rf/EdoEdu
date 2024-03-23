import flask

from .db import get_db
from .auth import login_required

blog_bp = flask.Blueprint('blog', __name__)


@blog_bp.route('/')
@login_required()
def index():
    db = get_db()
    posts = db.execute(
        """
            SELECT p.id, p.author_id, u.username, p.title, p.body, p.created
            from post p JOIN user u ON p.author_id = u.id
            ORDER BY created DESC
        """
    ).fetchall()
    return flask.render_template('blog/index.html', posts=posts)


@blog_bp.route('/create', methods=('GET', 'POST'))
@login_required()
def create():
    import datetime as dt

    if flask.request.method == 'GET':
        return flask.render_template('blog/create.html')
    else:
        title = flask.request.form['title']
        body = flask.request.form['body']

        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flask.flash(error)
            return flask.redirect(flask.url_for('blog.create'))
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id) VALUES (?, ?, ?)',
                (title, body, flask.g.user['id'])
            )
            db.commit()
            return flask.redirect(flask.url_for('blog.index'))
