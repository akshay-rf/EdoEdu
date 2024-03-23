import flask
from flask import cli
import click

import sqlite3


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


def init_db():
    db = get_db()

    with flask.current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


def get_db():
    if 'db' not in flask.g:
        flask.g.db = sqlite3.connect(
            database=flask.current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )

        flask.g.db.row_factory = sqlite3.Row

    return flask.g.db


def close_db(e=None):
    db = flask.g.pop('db', None)

    if db is not None:
        db.close()


@click.command('init-db')
@cli.with_appcontext
def init_db_command():
    """
        Clear the existing data and create new tables.
    """
    init_db()
    click.echo('Initialized the database.')
