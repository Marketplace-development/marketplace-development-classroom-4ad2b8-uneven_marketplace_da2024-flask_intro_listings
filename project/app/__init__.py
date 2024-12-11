from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import Config  # Zorg dat Config wordt geïmporteerd

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)

    # Configuratie
    app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = Config.SQLALCHEMY_TRACK_MODIFICATIONS
    app.config['SECRET_KEY'] = Config.SECRET_KEY

    # Initialiseer extensies
    db.init_app(app)
    migrate.init_app(app, db)

    # Registreer blueprints
    from .routes import main
    app.register_blueprint(main)

    with app.app_context():
        from .models import Category
        default_categories = [
            "Luxereis", "Budgetreis", "Backpacken", "Wandelreis",
            "Skireis", "Familiereis", "Strandvakantie", "Citytrip",
            "Cultuurreis", "Kampeertrip", "Roadtrip", "Natuur", "Avontuurlijk", "Culinair",
            "Fietsvakantie", "Cruise", "Andere"
        ]
        for category_name in default_categories:
            if not Category.query.filter_by(name=category_name).first():
                db.session.add(Category(name=category_name))
        db.session.commit()

    return app


