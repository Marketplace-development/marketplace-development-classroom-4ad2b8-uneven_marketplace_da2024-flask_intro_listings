# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import Config
from .models import db
from .routes import bp

migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
# this registers the routes defined in routes.py
    app.register_blueprint(bp)

    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        from .routes import main
        app.register_blueprint(main)

    return app
