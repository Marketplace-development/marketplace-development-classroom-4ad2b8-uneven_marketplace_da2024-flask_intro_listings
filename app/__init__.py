from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import Config
from .models import db, User, Listing
from flask_login import LoginManager


migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        from .routes import main
        from .chat import chat  # Import chat blueprint
        app.register_blueprint(main)
        app.register_blueprint(chat, url_prefix='/helpdesk')  # Register chat blueprint

    login_manager = LoginManager(app)
    login_manager.login_view = 'main.login'
    login_manager.login_message = "Please log in to access this page."
    login_manager.login_message_category = 'info'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app