import sys
from os import path

# Voeg de map 'project' toe aan sys.path
sys.path.append(path.join(path.dirname(__file__), 'project'))

from app import create_app  # Importeer create_app vanuit de app-module

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
