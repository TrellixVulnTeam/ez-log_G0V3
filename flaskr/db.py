# import sqlite3
import psycopg2
import os

import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    if 'db' not in g:
        # g.db = sqlite3.connect(
        #     current_app.config['DATABASE'],
        #     detect_types=sqlite3.PARSE_DECLTYPES
        # )
        # g.db.row_factory = sqlite3.Row
        DATABASE_URL = os.environ['DATABASE_URL']
        # DATABASE_URL = os.environ.get('DATABASE_URL')
        g.db = psycopg2.connect(DATABASE_URL, sslmode='require')
    # print("DBDBDBDB: ", g.db)
    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()
    # db.set_session(autocommit=True)

    cursor = db.cursor()
    print(cursor)
    with current_app.open_resource('schema.sql') as f:
        cursor.execute(f.read().decode('utf8'))
    db.commit()

    # with current_app.open_resource('schema.sql') as f:
    #     db.executescript(f.read().decode('utf8'))

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Initialized the database.')
