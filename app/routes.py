# app/routes.py
from flask import Blueprint, request, redirect, url_for, render_template, session
from .models import db, Customer
from app.models import Customer, Recipe

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
bp = Blueprint("routes", __name__)

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

@bp.route("/add-recipe", methods=["GET", "POST"])
def add_recipe():
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        ingredients = request.form.get("ingredients")
        steps = request.form.get("steps")
        image = request.files.get("image")  # Optional image upload

        # For now, just print the recipe data to the console
        print(f"Title: {title}")
        print(f"Description: {description}")
        print(f"Ingredients: {ingredients}")
        print(f"Steps: {steps}")

        # Save the image if uploaded
        if image:
            image.save(f"static/uploads/{image.filename}")
            print(f"Image saved as static/uploads/{image.filename}")

        return render_template("thank_you.html", title=title)

    return render_template("add-recipe.html")

@bp.route('/contact')
def contact():
    return render_template('contactpage.html')

@bp.route('/about')
def about():
    return render_template('about.html')

