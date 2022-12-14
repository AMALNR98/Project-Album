import click
from flask import Flask
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import configure_uploads
from flask_cors import CORS
from .auth import auth_bp, login_manager
from .album_app import album_bp, uploaded_images
from .database import db
from album import filters


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../database.db"
    app.config["UPLOADED_PHOTOS_DEST"] = "album/static/users"
    filters.add_filter(app)
    app.secret_key = "dev"
    db.init_app(app)
    login_manager.init_app(app)
    CORS(app)
    configure_uploads(app, uploaded_images)
    app.register_blueprint(auth_bp)
    app.register_blueprint(album_bp)
    app.cli.add_command(init_db)
    app.secret_key = "rff"
    return app


@click.command("init-db")
@with_appcontext
def init_db():
    db.drop_all()
    db.create_all()
    click.echo("Initialized databases")
