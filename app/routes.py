from flask import Blueprint, request, redirect, url_for, render_template, session, flash
from .models import db, User, Vendor #, Listing # Als comment aangezien deze klasse ook als comment staat in models
from .models import MealOffering, Review, CuisineType   #hoort bij ons algoritme

main = Blueprint('main', __name__)

@main.route('/register', methods=['GET', 'POST'])
def register():
    print(f"Session user_id: {session.get('user_id')}")  # Toont de opgeslagen session user_id

    if request.method == 'POST':
        username = request.form['username']  # Haal de gebruikersnaam op uit het formulier
        email = request.form['email']
        street = request.form['street']
        house_number = request.form['house number']
        postal_code = request.form['postal code']
        city = request.form['city']


        # Controleer of de gebruiker al bestaat in de database
        if User.query.filter_by(username=username).first() is None:
            # Als de gebruiker niet bestaat, voeg deze toe aan de database
            new_user = User(
                username=username,
                email=email,
                street=street,
                house_number=house_number,
                postal_code=postal_code,
                city=city,
                type='user'  # Standaardwaarde
            )
                
            db.session.add(new_user)
            db.session.commit()  # Sla de gebruiker op in de database

            # Zet de gebruiker in de sessie (om automatisch ingelogd te zijn)
            session['user_id'] = new_user.id
            flash("User registered successfully!", "success")

            # Redirect naar de indexpagina (na succesvolle registratie)
            return redirect(url_for('main.index'))
        else:
            flash("User already exists, try a different name.", "error")  # Toon foutmelding
            return redirect(url_for('main.register'))  # Herlaad de registratiepagina als de naam al bestaat

    return render_template('2. Signup.html')  # Render de registratiepagina (GET-request)


# Login route: gebruikers kunnen zich hier aanmelden met hun gebruikersnaam
@main.route('/login', methods=['GET', 'POST'])
def login():
    print(f"Session user_id: {session.get('user_id')}")  # Toont de opgeslagen session user_id

    if request.method == 'POST':
        username = request.form['username']
        user = User.query.filter_by(username=username).first()  # Zoek de gebruiker in de database
        if user:
            session['user_id'] = user.id  # Zet de gebruiker in de sessie
            return redirect(url_for('main.index'))  # Redirect naar de indexpagina
        flash("User not found, please try again")  # Toon een foutmelding als de gebruiker niet bestaat
    return render_template('1.Login.html')  # Toon de loginpagina

# Logout route: gebruiker kan uitloggen
@main.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)  # Verwijder de gebruiker uit de sessie
    return redirect(url_for('main.login'))  # Na uitloggen, stuur naar de loginpagina


@main.route('/base')
def base():
    return render_template('base.html')

@main.route('/add-meal', methods=['GET', 'POST'])
def add_meal():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        picture = request.files['picture'] if 'picture' in request.files else None
        status = request.form['status']  # Dit is automatisch ingesteld op "Beschikbaar"
        username = request.form['username']
        user = User.query.filter_by(username=username).first()  # Zoek de gebruiker in de database
        if user:
            session['user_id'] = user.id  # Zet de gebruiker in de sessie
        vendor_id = session['user_id'] # De ingelogde gebruiker wordt als verkoper toegevoegd
        cuisine = request.form['cuisine']
        #categories = request.form.getlist('categories')
        #categories verwijdert in models.py -> dus niet meer nodig

        # Verwerk de afbeelding (optioneel)
        picture_filename = None
        if picture:
            picture_filename = f"static/images/{picture.filename}"
            picture.save(picture_filename)

        # Nieuwe maaltijd toevoegen aan de database
        new_meal = MealOffering(
            name=name,
            description=description,
            picture=picture_filename,
            status=status,
            vendor_id=vendor_id,
            cuisine=CuisineType[cuisine] #aanpassing lijn na verwijderen categories
            )

        db.session.add(new_meal)
        db.session.commit()

        # Koppel de maaltijd aan de geselecteerde categorieën
        #code hieronder niet meer nodig doordat category verwijderd is
        #for category_id in categories:
        #    category = Category.query.get(category_id)
        #    new_meal.categories.append(category)
        #db.session.commit()

        return redirect(url_for('main.index'))

    vendors = Vendor.query.all()  # Dit kan eventueel weggehaald worden, omdat we vendor_id automatisch vullen.
    #categories = Category.query.all() -> ook niet meer nodig
    return render_template('4.Meal_Creation.html', categories=CuisineType)



#Begin van algoritme filteren op keuken/stad/beoordeling
@main.route('/', methods=['GET', 'POST'])
def index():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])  # Haal de ingelogde gebruiker op
        city = user.city  # Haal de stad van de ingelogde gebruiker op
        cuisine_filter = request.args.get('cuisine', None)  # Haal het cuisine filter op
        
        # Haal alle maaltijden (MealOffering) op en filteren op cuisine
        meal_offerings = MealOffering.query.all()

        # Filteren op cuisine (keuken)
        if cuisine_filter:
            meal_offerings = [meal for meal in meal_offerings if meal.cuisine == CuisineType[cuisine_filter]]

        # Filteren op stad
        local_meals = [meal for meal in meal_offerings if meal.vendor.city == city]  # Lokale maaltijden
        other_meals = [meal for meal in meal_offerings if meal.vendor.city != city]  # Andere maaltijden
        meal_offerings_sorted = local_meals + other_meals  # Lokale maaltijden bovenaan

        # Bereken de gemiddelde beoordeling voor maaltijden
        def get_average_rating(meal_id):
            reviews = Review.query.filter_by(meal_id=meal_id).all()
            if reviews:
                total_score = sum(review.score for review in reviews)
                return total_score / len(reviews)
            return 0

        # Sorteer maaltijden op basis van beoordeling
        meal_offerings_sorted = sorted(meal_offerings_sorted, key=lambda meal: get_average_rating(meal.meal_id), reverse=True)

        return render_template('index.html', username=user.username, listings=meal_offerings_sorted)
    else:
        return redirect(url_for('main.login'))  # Als de gebruiker niet is ingelogd, stuur naar loginpagina
