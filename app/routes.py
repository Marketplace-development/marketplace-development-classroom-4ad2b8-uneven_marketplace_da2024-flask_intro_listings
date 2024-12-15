# app/routes.py
from flask import Blueprint, request, redirect, url_for, render_template, session, jsonify, flash
from app.models import Customer, Recipe, Favorite, UserRecipe, Ingredient, Rating
from .forms import TitleForm, DescriptionForm, IngredientsForm, StepsForm, PriceForm
from .models import db, Customer
from flask import current_app

main = Blueprint('main', __name__)

@main.route('/')
def index():
    if 'user_id' in session:
        user = Customer.query.get(session['user_id'])
        return render_template('index.html', username=user.username)
    return render_template('index.html', username=None)

@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        if Customer.query.filter_by(username=username).first() is None:
            new_user = Customer(username=username)
            db.session.add(new_user)
            db.session.commit()
            session['user_id'] = new_user.id
            return redirect(url_for('main.index'))
        return 'Username already registered'
    return render_template('register.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        user = Customer.query.filter_by(username=username).first()
        if user:
            session['user_id'] = user.id
            return redirect(url_for('main.index'))
        return 'User not found'
    return render_template('login.html')

@main.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return redirect(url_for('main.index'))


# creates a route for the homepage
# We import Blueprint system for route management
from flask import Blueprint
bp = Blueprint("routes", __name__, template_folder='templates')

@bp.route("/")
def home():
    return render_template("home_page.html")

# Simulated database
users = []

# Login Page
@bp.route("/login", methods=["GET", "POST"])
def login():
    error_message = None  # To store login error messages

    if request.method == "POST":
        # Retrieve login form data
        username = request.form.get("username")

        # Check if the username exists in the database
        user = Customer.query.filter_by(username=username).first()

        if user:
            # Successful login, save user ID to the session
            session["user_id"] = user.customer_id
            session["username"] = user.username
            return redirect(url_for("routes.account"))
        else:
            # Username doesn't exist
            error_message = "Invalid username. Please try again."

    return render_template("login.html", error_message=error_message)

# Logout Route
@bp.route("/logout", methods=["POST"])
def logout():
    # Clear the user session
    session.clear()
    return redirect(url_for("routes.login"))

# Adjust the My Account Route
@bp.route("/account")
def account():
    # Ensure a user is logged in
    if "user_id" not in session:
        return redirect(url_for("routes.login"))

    # Fetch the logged-in user's data
    user = Customer.query.get(session["user_id"])
    if not user:
        return redirect(url_for("routes.login"))  # Redirect if user doesn't exist

    # Pass user data to the dashboard template
    return render_template("dashboard.html", user=user)

@bp.route("/signup", methods=["GET", "POST"])
def signup():
    error_username = None  # Error message for the username

    if request.method == "POST":
        # Retrieve form data
        username = request.form.get("username")
        email = request.form.get("email")
        dob = request.form.get("dob")
        address = request.form.get("address")
        city = request.form.get("city")
        postcode = request.form.get("postcode")
        country = request.form.get("country")
        language = request.form.get("language")

        # Check if the username already exists
        existing_user = Customer.query.filter_by(username=username).first()
        if existing_user:
            error_username = "Username is already taken. Please choose a different one."
            return render_template(
                "signup.html",
                error_username=error_username,
                username=username,
                email=email,
                dob=dob,
                address=address,
                city=city,
                postcode=postcode,
                country=country,
                language=language,
            )

        # Create a new customer object
        new_customer = Customer(
            username=username,
            email=email,
            date_of_birth=dob,
            address=address,
            city=city,
            country=country,
            postcode=postcode,
            language=language,
        )

        # Add the new customer to the database
        try:
            db.session.add(new_customer)
            db.session.commit()
            return redirect(url_for("routes.login"))  # Redirect to login page after successful signup
        except Exception as e:
            db.session.rollback()
            error_message = f"An error occurred: {e}"
            return render_template("signup.html", error_message=error_message)

    return render_template("signup.html")

@bp.route("/privacy-policy")
def privacy_policy():
    return render_template("privacy-policy.html")

@bp.route("/terms-of-service")
def terms_of_service():
    return render_template("terms-of-service.html")

@bp.route("/dashboard")
def dashboard():
    # Check if the user is logged in
    if "user_id" not in session:
        return redirect(url_for("routes.login"))

    # Fetch the logged-in user's details from the database
    user = Customer.query.get(session["user_id"])

    # Fetch additional user-specific data (e.g., their submitted recipes and favorite recipes)
    submitted_recipes = Recipe.query.filter_by(user_id=user.customer_id).all()
    favorite_recipes = []  # Placeholder if you decide to implement a favorites system later

    # Render the dashboard with dynamic user data
    return render_template(
        "dashboard.html",
        user=user,
        submitted_recipes=submitted_recipes,
        favorite_recipes=favorite_recipes
    )


@bp.route("/subscribe", methods=["POST"])
def subscribe():
    email = request.form.get("email")
    if email:
        # Example: Save the email to a database or send a confirmation email
        print(f"New subscriber: {email}")
    return redirect("/")  # Redirect back to the homepage

@bp.route('/contact')
def contact():
    return render_template('contactpage.html')

@bp.route('/about')
def about():
    return render_template('about.html')

@bp.route('/recipes')
def list_recipes():
    recipes = Recipe.query.all()  # Fetch all recipes from the database
    return render_template('recipes.html', recipes=recipes)

from sqlalchemy import func  # Import SQLAlchemy's func

@bp.route('/submitted-recipes')
def submitted_recipes():
    # Ensure the user is logged in
    if 'user_id' not in session:
        return redirect(url_for('routes.login'))

    user_id = session['user_id']

    # Fetch the logged-in user
    user = db.session.query(Customer).filter_by(customer_id=user_id).first()
    if not user:
        return "User not found", 404

    # Handle search and region filters
    search_term = request.args.get('search', '').strip().lower()
    selected_region = request.args.get('region', '').strip().lower()

    # Base query: filter recipes by the logged-in user
    query = db.session.query(Recipe).filter_by(user_id=user_id)

    if search_term:
        query = query.filter(func.lower(Recipe.title).contains(search_term))  # Case-insensitive search

    if selected_region:
        # Use func.lower on both sides to ensure case-insensitive matching
        query = query.filter(func.lower(Recipe.region) == selected_region)

    # Fetch recipes with favorite status
    recipes = query.all()
    favorite_recipe_ids = {fav.recipe_id for fav in db.session.query(Favorite).filter_by(user_id=user_id).all()}

    # Mark each recipe with its favorite status
    for recipe in recipes:
        recipe.is_favorite = recipe.recipe_id in favorite_recipe_ids

    # Fetch unique regions for the filter dropdown (convert to lowercase for consistency)
    unique_regions = [row[0] for row in db.session.query(func.distinct(func.lower(Recipe.region))).all() if row[0]]

    return render_template(
        'submitted_recipes.html',
        user=user,
        recipes=recipes,
        unique_regions=unique_regions
    )

@bp.route('/favorites', methods=['GET'])
def favorites():
    if 'user_id' not in session:
        return redirect(url_for('routes.login'))

    user_id = session['user_id']

    # Fetch user information
    user = db.session.query(Customer).filter_by(customer_id=user_id).first()
    if not user:
        return "User not found", 404

    # Get search and region filters
    search_term = request.args.get('search', '').lower()
    selected_region = request.args.get('region', '').lower()

    # Query the user's favorite recipes
    query = (
        db.session.query(Recipe)
        .join(Favorite, Recipe.recipe_id == Favorite.recipe_id)
        .filter(Favorite.user_id == user_id)
    )

    if search_term:
        query = query.filter(func.lower(Recipe.title).contains(search_term))  # Case-insensitive search

    if selected_region:
        query = query.filter(func.lower(Recipe.region) == selected_region)  # Ensure case-insensitive comparison

    favorite_recipes = query.all()

    # Fetch unique regions for the filter dropdown
    unique_regions = [
        row[0].capitalize()
        for row in db.session.query(func.distinct(func.lower(Recipe.region))).all()
    ]

    return render_template(
        'favorites.html',
        user=user,
        favorites=favorite_recipes,
        unique_regions=unique_regions
    )

@bp.route('/favorites/toggle', methods=['POST'])
def toggle_favorite():
    if 'user_id' not in session:
        return jsonify({"success": False, "message": "User not logged in"}), 401

    user_id = session['user_id']
    recipe_id = request.json.get('recipe_id')

    if not recipe_id:
        return jsonify({"success": False, "message": "Invalid recipe ID"}), 400

    # Check if the recipe is already a favorite
    favorite = Favorite.query.filter_by(user_id=user_id, recipe_id=recipe_id).first()

    if favorite:
        # Remove from favorites
        db.session.delete(favorite)
        db.session.commit()
        return jsonify({"success": True, "message": "Removed from favorites", "is_favorite": False}), 200
    else:
        # Add to favorites
        new_favorite = Favorite(user_id=user_id, recipe_id=recipe_id)
        db.session.add(new_favorite)
        db.session.commit()
        return jsonify({"success": True, "message": "Added to favorites", "is_favorite": True}), 201

@bp.route('/edit-profile', methods=['GET', 'POST'])
def edit_profile():
    # Ensure the user is logged in
    if 'user_id' not in session:
        return redirect(url_for('routes.login'))

    user_id = session['user_id']
    user = db.session.query(Customer).filter_by(customer_id=user_id).first()

    if request.method == 'POST':
        # Update user information
        user.username = request.form['username']
        user.email = request.form['email']
        user.date_of_birth = request.form['date_of_birth']
        user.country = request.form['country']
        user.language = request.form['language']

        try:
            db.session.commit()
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('routes.dashboard'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while updating your profile.', 'error')

    return render_template('edit_profile.html', user=user)

import os
from werkzeug.utils import secure_filename

@bp.route('/add-recipe/title', methods=['GET', 'POST'])
def add_recipe_title():
    form = TitleForm()
    if form.validate_on_submit():
        session['title'] = form.title.data
        # Verwerk de foto indien aanwezig
        if form.photo.data:
            filename = secure_filename(form.photo.data.filename)
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            form.photo.data.save(filepath)
            session['image_url'] = filename
            # Sla de foto op op de gewenste locatie
        else:
            session['image_url'] = None  # Stel expliciet in als None
        return redirect(url_for('routes.add_recipe_description'))
    return render_template('add_recipe/title.html', form=form)

@bp.route('/add-recipe/description', methods=['GET', 'POST'])
def add_recipe_description():
    form = DescriptionForm()
    if form.validate_on_submit():
        session['description'] = form.description.data
        return redirect(url_for('routes.add_recipe_ingredients'))
    
    # Debug: Print foutmeldingen van validatie
    if form.errors:
        print("Form validation errors:", form.errors)
    
    return render_template('add_recipe/description.html', form=form)

@bp.route('/add-recipe/ingredients', methods=['GET', 'POST'])
def add_recipe_ingredients():
    form = IngredientsForm()
    if form.validate_on_submit():
        session['ingredients'] = form.ingredients.data
        return redirect(url_for('routes.add_recipe_steps'))
    return render_template('add_recipe/ingredients.html', form=form)

@bp.route('/add-recipe/steps', methods=['GET', 'POST'])
def add_recipe_steps():
    form = StepsForm()
    if form.validate_on_submit():
        session['steps'] = form.steps.data

        # Opslaan in de database
        new_recipe = Recipe(
            title=session.get('title'),
            description=session.get('description'),
            ingredients=session.get('ingredients'),
            steps=session.get('steps')
        )
        db.session.add(new_recipe)
        db.session.commit()

        # Doorsturen naar de bevestigingspagina
        return redirect(url_for('routes.add_recipe_confirmation'))

    # Als het formulier niet gevalideerd is, blijf op de pagina
    return render_template('add_recipe/steps.html', form=form)

@bp.route('/add-recipe/price', methods=['GET', 'POST'])
def add_recipe_price():
    form = PriceForm()
    if form.validate_on_submit():
        session['price'] = form.price.data
        return redirect(url_for('routes.add_recipe_confirmation'))
    return render_template('add_recipe/price.html', form=form)

@bp.route('/add-recipe/confirmation', methods=['GET', 'POST'])
def add_recipe_confirmation():
    # Haal alle gegevens op uit de sessie
    title = session.get('title')
    description = session.get('description')
    ingredients = session.get('ingredients')
    steps = session.get('steps')
    price = session.get('price')
    image_url = session.get('image_url')

    if request.method == 'POST':
        # Opslaan van recept in de database (voorbeeldcode)
        new_recipe = UserRecipe(
            title=title,
            description=description,
            price=price,
            steps=steps,
            ingredients=ingredients,
            image_url=image_url
        )
        db.session.add(new_recipe)
        db.session.commit()

        # Reset de sessie
        session.clear()
        return redirect(url_for('routes.submitted_recipes'))

    return render_template('add_recipe/confirmation.html', title=title, description=description, ingredients=ingredients, steps=steps, price=price, image_url=image_url)

@bp.route('/recipe/<int:recipe_id>', methods=['GET'])
def recipe_page(recipe_id):
    # Haal het recept op uit de database
    recipe = Recipe.query.get(recipe_id)
    if not recipe:
        return render_template('404.html', message="Recipe not found"), 404

    # Haal de gebruiker op die het recept heeft gemaakt
    creator = Customer.query.get(recipe.user_id)
    if not creator:
        return render_template('404.html', message="Creator not found"), 404

    # Haal de reviews en ratings van het recept op
    reviews = db.session.query(Rating).filter_by(recipe_id=recipe_id).all()

    # Controleer of een gebruiker is ingelogd
    user = None
    if 'user_id' in session:
        user = Customer.query.get(session['user_id'])

    # Controleer of het recept favoriet is van de ingelogde gebruiker
    is_favorite = (
        bool(Favorite.query.filter_by(user_id=user.customer_id, recipe_id=recipe_id).first())
        if user else False
    )

    # Render de `recipe_page.html` template met de opgehaalde data
    return render_template(
        'recipe_page.html',
        recipe=recipe,
        creator=creator,
        reviews=reviews,
        user=user,
        is_favorite=is_favorite,
    )

from flask import render_template, request
from app.models import Recipe

@bp.route('/recipe/<int:recipe_id>', methods=['GET'])
def recipe_detail(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)  # Haal het recept op uit de database
    creator = recipe.creator  # Creator van het recept
    reviews = recipe.reviews  # Reviews voor dit recept
    is_favorite = False  # Voeg logica toe voor favoriete recepten
    
    return render_template('recipe_detail.html', recipe=recipe, creator=creator, reviews=reviews, is_favorite=is_favorite)
