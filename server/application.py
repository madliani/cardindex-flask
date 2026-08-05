from flask import Blueprint, Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


def make_app(
    bp: Blueprint, db: SQLAlchemy, migrate: Migrate, postgres_uri: str
) -> Flask:
    """Flask application factory."""

    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = postgres_uri

    app.register_blueprint(bp)
    db.init_app(app)
    migrate.init_app(app=app, db=db)

    return app
