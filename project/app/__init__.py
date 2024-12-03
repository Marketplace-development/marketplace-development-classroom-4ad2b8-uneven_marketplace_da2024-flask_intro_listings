from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'

    # Voeg routes toe
    from .routes import main  # Zorg ervoor dat de blueprint 'main' correct is gedefinieerd
    app.register_blueprint(main)

    return app




