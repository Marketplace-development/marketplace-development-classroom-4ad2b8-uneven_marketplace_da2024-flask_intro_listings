from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # Set the secret key for session management and security
    app.secret_key = "my-school-project-key"  # You can customize this key if desired.

    # Load configurations from the Config class
    app.config.from_object("app.config.Config")

    # Initialize the SQLAlchemy instance
    db.init_app(app)
    migrate.init_app(app, db)


    # Register blueprints
    from .routes import bp as main_bp
    app.register_blueprint(main_bp)

    return app