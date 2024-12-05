# app/routes.py
from flask import Blueprint, render_template
from flask import Blueprint, request, redirect, url_for, render_template, session
from .models import db, User
from flask import Blueprint, render_template, request, redirect, url_for

main = Blueprint('main', __name__)

@main.route('/')
def index():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        return render_template('index.html', username=user.username)
    return render_template('index.html', username=None)

@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        if User.query.filter_by(username=username).first() is None:
            new_user = User(username=username)
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
        user = User.query.filter_by(username=username).first()
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
    if request.method == "POST":
        username = request.form.get("username")
        # Check if username exists in the database
        if username in [user["username"] for user in users]:
            return redirect(url_for("routes.home"))
        else:
            # Redirect to signup with an error message
            return redirect(url_for("routes.signup", error="Username not found. Please sign up."))
    return render_template("login.html")

# Signup Page
@bp.route("/signup", methods=["GET", "POST"])
def signup():
    error = request.args.get("error", None)
    if request.method == "POST":
        # Retrieve form data
        username = request.form.get("username")
        full_name = request.form.get("full_name")
        email = request.form.get("email")
        dob = request.form.get("dob")
        address = request.form.get("address")
        city = request.form.get("city")
        postcode = request.form.get("postcode")
        country = request.form.get("country")
        language = request.form.get("language")
        
        # Example: Save this data to the database (you'll need a database connection)
        # db.insert_user(username, full_name, email, dob, address, city, postcode, country, language)

        return redirect(url_for("routes.login"))
    return render_template("signup.html", error=error)

@bp.route("/privacy-policy")
def privacy_policy():
    return render_template("privacy-policy.html")

@bp.route("/terms-of-service")
def terms_of_service():
    return render_template("terms-of-service.html")

@bp.route("/dashboard")
def dashboard():
    # Dummy data for now (to simulate real user data)
    user_info = {
        "username": "JohnDoe",
        "email": "johndoe@example.com",
        "address": "123 Foodie Lane",
        "city": "Gourmet City",
        "postcode": "12345",
    }

    recent_activity = [
        {"title": "Spaghetti Carbonara", "link": "/recipe/1"},
        {"title": "Chicken Tikka Masala", "link": "/recipe/2"},
        {"title": "Chocolate Lava Cake", "link": "/recipe/3"},
    ]

    favorite_recipes = [
        {"title": "Homemade Pizza", "link": "/recipe/4"},
        {"title": "Beef Stroganoff", "link": "/recipe/5"},
    ]

    return render_template(
        "dashboard.html",
        user_info=user_info,
        recent_activity=recent_activity,
        favorite_recipes=favorite_recipes,
    )

@bp.route("/account")
def account():
    return render_template("dashboard.html")

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

