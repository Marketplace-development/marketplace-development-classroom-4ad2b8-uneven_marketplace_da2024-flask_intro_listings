# app/routes.py
from flask import Blueprint, request, redirect, url_for, render_template, session, flash
from .models import db, Customer, Recipe, UserRecipe, Ingredient
from app.models import Customer, Recipe
from .forms import TitleForm, DescriptionForm, IngredientsForm, StepsForm
from flask import render_template, redirect, url_for, session, request

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

@bp.route('/submitted-recipes')
def submitted_recipes():
    try:
        # Fetch the logged-in user's ID from the session
        user_id = session.get('user_id')

        # If no user is logged in, redirect to the login page
        if not user_id:
            return redirect(url_for('routes.login'))

        # Query recipes based on the logged-in user's ID
        recipes = Recipe.query.filter_by(user_id=user_id).all()
        return render_template('submitted_recipes.html', recipes=recipes)
    except Exception as e:
        return f"An error occurred: {e}"

@bp.route("/favorites")
def favorites():
    return "Favorites Page"  # Placeholder

from flask import render_template, redirect, url_for, session, request

@bp.route('/add-recipe/title', methods=['GET', 'POST'])
def add_recipe_title():
    form = TitleForm()
    if form.validate_on_submit():
        session['title'] = form.title.data
        # Verwerk de foto indien aanwezig
        if form.photo.data:
            photo = form.photo.data
            # Sla de foto op op de gewenste locatie
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

@bp.route('/add-recipe/confirmation')
def add_recipe_confirmation():
    # Haal de gegevens op uit de sessie om te bevestigen
    title = session.get('title')
    description = session.get('description')
    ingredients = session.get('ingredients')
    steps = session.get('steps')
    return render_template('add_recipe/confirmation.html', title=title, description=description, ingredients=ingredients, steps=steps)

