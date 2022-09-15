import click
from flask import Flask 
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy

from .auth import auth_bp
from .album_app import album_bp


db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../database.db'
    db.init_app(app)
    app.register_blueprint(auth_bp)
    app.register_blueprint(album_bp)
    app.cli.add_command(init_db)
    app.secret_key = 'rff'
    return app


@click.command("init-db")
@with_appcontext
def init_db():
    db.drop_all()
    db.create_all()
    click.echo("Initialized databases")

    