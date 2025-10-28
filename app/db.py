# logic to connect with database
import sqlite3
from datetime import datetime
import click
# current_app is object that points to Flask application
# g is another special object unique for each request
from flask import current_app, g


# connects to database
def get_db():

    if 'db' not in g:
        # connect establishes connection to file pointer by DATABASE configuration key
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    
    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

# reads schema file to create tables
def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
def init_db_command():
    # Clear the existing data and create new tables.
    init_db()
    click.echo('Initialized the database.')

# not to sure what this does got it from documentation
sqlite3.register_converter(
    "timestamp", lambda v: datetime.fromisoformat(v.decode())
)

def init_app(app):
    # after every request close database connection automatically
    app.teardown_appcontext(close_db)
    # registers 'flask init-db' command
    app.cli.add_command(init_db_command)