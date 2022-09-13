import click
from flask import Flask 
from flask.cli import with_appcontext

from .database import db 

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../database.db'
    db.init_app(app)
    app.cli.add_command(init_db)
    return app


@click.command("init-db")
@with_appcontext
def init_db():
    db.drop_all()
    db.create_all()
    click.echo("Initialized databases")

    