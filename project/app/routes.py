# app/routes.py

import datetime
import uuid
from flask import Blueprint, request, redirect, url_for, render_template, session
from .models import db, Users

main = Blueprint('main', __name__)

@main.route('/')
def index():
    if 'userid' in session:
        user = Users.query.get(session['userid'])
        return render_template('index.html', username=user.username)
    return render_template('index.html', username=None)

@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Haal gegevens op uit het formulier
        email = request.form.get('email')
        password = request.form.get('password')  # Zorg dat je wachtwoord veilig opslaat!
        first_name = request.form.get('firstname')
        last_name = request.form.get('lastname')
        birth_date = request.form.get('birthdate')
        address = request.form.get('address')
        city = request.form.get('city')
        postal_code = request.form.get('postalcode')
        country = request.form.get('country')
        phone = request.form.get('phone')
        nationality = request.form.get('nationality')

        # Controleer of de gebruiker al bestaat op basis van email of username
        if Users.query.filter((Users.email == email)).first():
            return "Email or Username already registered", 400

        # Maak een nieuwe gebruiker aan
        new_user = Users(
            userid=str(uuid.uuid4()),  # Genereer een unieke ID
            email=email,
            password=password,  # Hash het wachtwoord
            firstname=first_name,
            lastname=last_name,
            birthdate=datetime.datetime.strptime(birth_date, '%Y-%m-%d') if birth_date else None,
            address=address,
            city=city,
            postalcode=postal_code,
            country=country,
            phone=phone,
            nationality=nationality
        )

        # Voeg de gebruiker toe aan de database
        db.session.add(new_user)
        db.session.commit()

        # Sla de userID op in de sessie
        session['userID'] = new_user.userID

        return redirect(url_for('main.index'))

    # Bij een GET-verzoek toon het registratieformulier
    else:
        return render_template('register.html')


@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        user = Users.query.filter_by(username=username).first()
        if user:
            session['userid'] = user.id
            return redirect(url_for('main.index'))
        return 'User not found'
    return render_template('login.html')

@main.route('/logout', methods=['POST'])
def logout():
    session.pop('userid', None)
    return redirect(url_for('main.index'))

@main.route('/post', methods=['GET', 'POST'])
def post():
    return render_template('post.html')

@main.route('/search', methods=['GET', 'POST'])
def search():
    return render_template('search.html')

@main.route('/registreer', methods=['GET', 'POST'])
def registreer():
    return render_template('register.html')
