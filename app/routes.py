# app/routes.py
from flask import Blueprint, request, redirect, url_for, render_template, session, jsonify, flash, current_app
from app.models import Customer, Recipe, Favorite, Ingredient, Rating, ShoppingCart, PurchasedRecipe
from .forms import TitleForm, DescriptionForm, IngredientsForm, StepsForm, PriceForm, RecipeRegionForm, RecipeDurationForm, RatingForm
from .models import db, Customer

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
    search_term = request.args.get('search', '').lower()
    selected_region = request.args.get('region', '').lower()

    # Base query: filter recipes by the logged-in user
    query = db.session.query(Recipe).filter_by(user_id=user_id)

    if search_term:
        query = query.filter(func.lower(Recipe.title).contains(search_term))  # Case-insensitive search

    if selected_region:
        query = query.filter(func.lower(Recipe.region) == selected_region)  # Case-insensitive region filter

    # Fetch recipes with favorite status
    recipes = query.all()
    favorite_recipe_ids = {fav.recipe_id for fav in db.session.query(Favorite).filter_by(user_id=user_id).all()}

    # Ensure image_url is included for each recipe and mark favorite status
    for recipe in recipes:
        recipe.is_favorite = recipe.recipe_id in favorite_recipe_ids

    # Fetch unique regions for the filter dropdown
    unique_regions = [row[0] for row in db.session.query(func.distinct(func.lower(Recipe.region))).all()]

    return render_template(
        'submitted_recipes.html',
        user=user,
        recipes=recipes,  # Ensure `image_url` is part of recipes
        unique_regions=unique_regions
    )

@bp.route('/favorites', methods=['GET'])
def favorites():
    # Ensure the user is logged in
    if 'user_id' not in session:
        return redirect(url_for('routes.login'))

    user_id = session['user_id']

    # Fetch the user object
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
        query = query.filter(func.lower(Recipe.region) == selected_region)  # Case-insensitive region filter

    favorite_recipes = query.all()

    # Fetch unique regions for the filter dropdown
    unique_regions = [row[0] for row in db.session.query(func.distinct(func.lower(Recipe.region))).all()]

    # Pass the user and favorite recipes to the template
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
    try:
        # Ensure JSON payload exists
        data = request.get_json()
        if not data or 'recipe_id' not in data:
            return jsonify({"success": False, "message": "Invalid data provided"}), 400

        recipe_id = data.get('recipe_id')

        # Check if the recipe exists (optional sanity check)
        recipe = Recipe.query.get(recipe_id)
        if not recipe:
            return jsonify({"success": False, "message": "Recipe not found"}), 404

        # Check if the recipe is already in favorites
        favorite = Favorite.query.filter_by(user_id=user_id, recipe_id=recipe_id).first()

        if favorite:
            # Remove from favorites
            db.session.delete(favorite)
            db.session.commit()
            return jsonify({
                "success": True, 
                "message": "Removed from favorites", 
                "is_favorite": False
            }), 200
        else:
            # Add to favorites
            new_favorite = Favorite(user_id=user_id, recipe_id=recipe_id)
            db.session.add(new_favorite)
            db.session.commit()
            return jsonify({
                "success": True, 
                "message": "Added to favorites", 
                "is_favorite": True
            }), 201

    except Exception as e:
        print(f"Error in toggle_favorite: {e}")
        return jsonify({"success": False, "message": "An unexpected error occurred"}), 500

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
    print("Session values:", dict(session))

    # Fetch user_id from session
    if 'user_id' not in session:
        flash("You must be logged in to add a recipe.", "danger")
        return redirect(url_for('routes.login'))

    user_id = session.get('user_id')  # Fetch the logged-in user's ID

    # Retrieve all data from the session
    title = session.get('title')
    description = session.get('description')
    ingredients = session.get('ingredients')
    steps = session.get('steps')
    region = session.get('region')
    duration = session.get('duration')
    price = session.get('price')
    image_url = session.get('image_url')

    if request.method == 'POST':
        # Save recipe in the database with user_id
        new_recipe = Recipe(
            title=title,
            description=description,
            price=price,
            steps=steps,
            ingredients=ingredients,
            region=region,
            duration=duration,
            image_url=image_url,
            user_id=user_id  # Assign the logged-in user's ID
        )
        db.session.add(new_recipe)
        db.session.commit()

        # Clear the session data after saving
        session.pop('title', None)
        session.pop('description', None)
        session.pop('ingredients', None)
        session.pop('steps', None)
        session.pop('region', None)
        session.pop('duration', None)
        session.pop('price', None)
        session.pop('image_url', None)

        return redirect(url_for('routes.recipe_success'))

    return render_template(
        'add_recipe/confirmation.html',
        title=title,
        description=description,
        ingredients=ingredients,
        steps=steps,
        region=region,
        duration=duration,
        price=price,
        image_url=image_url
    )

@bp.route('/add-recipe/region', methods=['GET', 'POST'])
def add_recipe_region():
    form = RecipeRegionForm()
    if form.validate_on_submit():
        session['region'] = form.region.data
        return redirect(url_for('routes.add_recipe_duration'))
    return render_template('add_recipe/region.html', form=form)

@bp.route('/add-recipe/duration', methods=['GET', 'POST'])
def add_recipe_duration():
    form = RecipeDurationForm()
    if form.validate_on_submit():
        session['duration'] = form.duration.data
        return redirect(url_for('routes.add_recipe_price'))
    return render_template('add_recipe/duration.html', form=form)

@bp.route('/add-recipe/success', methods=['GET'])
def recipe_success():
    return render_template('add_recipe/success.html')

@bp.route('/recipe/<int:recipe_id>', methods=['GET'])
def recipe_page(recipe_id):
    # Query the database for the recipe
    recipe = Recipe.query.get_or_404(recipe_id)

    if not recipe:
        return render_template('404.html', message="Recipe not found"), 404

    # Fetch the creator of the recipe
    creator = Customer.query.get(recipe.user_id)

    # Fetch reviews for the recipe
    reviews = db.session.query(Rating).filter_by(recipe_id=recipe_id).all()

    # Check favorite status for logged-in user
    user = None
    is_favorite = False
    if 'user_id' in session:
        user = Customer.query.get(session['user_id'])
        is_favorite = bool(Favorite.query.filter_by(user_id=user.customer_id, recipe_id=recipe_id).first())

    return render_template(
        'recipe_page.html',
        recipe=recipe,
        creator=creator,
        reviews=reviews,
        is_favorite=is_favorite
    )

@bp.route('/recipe/<int:recipe_id>/add-review', methods=['GET', 'POST'])
def add_review(recipe_id):
    form = RatingForm()
    recipe = Recipe.query.get_or_404(recipe_id)
    customer_id = session.get('customer_id')  # Get the logged-in customer ID

    if not customer_id:
        flash('You need to log in to add a review.', 'danger')
        return redirect(url_for('routes.login'))

    if form.validate_on_submit():
        # Check for an existing review
        existing_rating = Rating.query.filter_by(recipe_id=recipe_id, customer_id=customer_id).first()
        if existing_rating:
            flash('You have already reviewed this recipe!', 'warning')
            return redirect(url_for('routes.view_recipe', recipe_id=recipe_id))
        
        # Add the new review
        new_rating = Rating(
            recipe_id=recipe_id,
            customer_id=customer_id,  # Use the logged-in user ID
            rating=form.rating.data,
            review=form.review.data
        )
        db.session.add(new_rating)
        db.session.commit()
        flash('Your review has been added!', 'success')
        return redirect(url_for('routes.view_recipe', recipe_id=recipe_id))
    
    # Fetch existing reviews for the template
    reviews = (
        db.session.query(Rating)
        .join(Customer, Rating.customer_id == Customer.customer_id)
        .filter(Rating.recipe_id == recipe_id)
        .all()
    )

    return render_template('reviews/add_review.html', form=form, recipe=recipe, reviews=reviews)


@bp.route('/add-to-cart', methods=['POST'])
def add_to_cart():
    if 'user_id' not in session:
        return jsonify({"success": False, "message": "User not logged in"}), 401

    data = request.get_json()
    if not data or 'recipe_id' not in data:
        return jsonify({"success": False, "message": "Invalid request"}), 400

    user_id = session['user_id']
    recipe_id = data['recipe_id']

    # Check if recipe already exists in cart
    existing_item = ShoppingCart.query.filter_by(user_id=user_id, recipe_id=recipe_id).first()
    if existing_item:
        return jsonify({"success": False, "message": "Recipe already in cart"}), 200

    # Add to cart
    new_item = ShoppingCart(user_id=user_id, recipe_id=recipe_id)
    db.session.add(new_item)
    db.session.commit()

    return jsonify({"success": True, "message": "Recipe added to cart!"}), 200

@bp.route('/cart', methods=['GET'])
def view_cart():
    if 'user_id' not in session:
        return redirect(url_for('routes.login'))

    user_id = session['user_id']
    cart_items = (
        db.session.query(Recipe)
        .join(ShoppingCart, Recipe.recipe_id == ShoppingCart.recipe_id)
        .filter(ShoppingCart.user_id == user_id)
        .all()
    )
    return render_template('cart.html', cart_items=cart_items)

@bp.route('/remove-from-cart', methods=['POST'])
def remove_from_cart():
    if 'user_id' not in session:
        return jsonify({"success": False, "message": "Not logged in"}), 401

    user_id = session['user_id']
    data = request.get_json()
    recipe_id = data.get("recipe_id")

    if not recipe_id:
        return jsonify({"success": False, "message": "Invalid recipe ID"}), 400

    # Find and delete the item
    item = ShoppingCart.query.filter_by(user_id=user_id, recipe_id=recipe_id).first()
    if item:
        db.session.delete(item)
        db.session.commit()
        return jsonify({"success": True, "message": "Recipe removed from cart"}), 200
    else:
        return jsonify({"success": False, "message": "Recipe not found in cart"}), 404 
    
@bp.route('/cart/purchase', methods=['POST'])
def purchase_recipes():
    if 'user_id' not in session:
        return jsonify({"success": False, "message": "User not logged in"}), 401

    user_id = session['user_id']

    # Get all items in the cart
    cart_items = ShoppingCart.query.filter_by(user_id=user_id).all()

    # Move each item to purchased_recipes
    for item in cart_items:
        purchased = PurchasedRecipe(user_id=user_id, recipe_id=item.recipe_id)
        db.session.add(purchased)
        db.session.delete(item)

    db.session.commit()
    return jsonify({"success": True, "message": "Purchase successful!"}), 200

@bp.route('/purchase-all', methods=['POST'])
def purchase_all():
    if 'user_id' not in session:
        return jsonify({"success": False, "message": "Not logged in"}), 401

    user_id = session['user_id']

    # Fetch all cart items for the user
    cart_items = ShoppingCart.query.filter_by(user_id=user_id).all()

    if not cart_items:
        return jsonify({"success": False, "message": "Your cart is empty"}), 400

    try:
        # Move items from ShoppingCart to PurchasedRecipe
        for cart_item in cart_items:
            purchased_recipe = PurchasedRecipe(user_id=user_id, recipe_id=cart_item.recipe_id)
            db.session.add(purchased_recipe)
            db.session.delete(cart_item)  # Remove from cart

        db.session.commit()
        return jsonify({"success": True, "message": "All items purchased successfully!"}), 200
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({"success": False, "message": "An error occurred while processing your purchase."}), 500

@bp.route('/purchased-recipes', methods=['GET'])
def purchased_recipes():
    if 'user_id' not in session:
        return redirect(url_for('routes.login'))

    user_id = session['user_id']

    # Fetch purchased recipes joined with Recipe table
    purchased_items = (
        db.session.query(Recipe)
        .join(PurchasedRecipe, Recipe.recipe_id == PurchasedRecipe.recipe_id)
        .filter(PurchasedRecipe.user_id == user_id)
        .all()
    )

    # Fetch user details for the sidebar
    user = db.session.query(Customer).filter_by(customer_id=user_id).first()

    return render_template(
        'purchased_recipes.html',
        purchased_items=purchased_items,
        user=user
    )

# This gives us the cart count
@bp.route('/cart-count', methods=['GET'])
def cart_count():
    if 'user_id' not in session:
        return jsonify({"success": True, "count": 0})

    user_id = session['user_id']
    count = ShoppingCart.query.filter_by(user_id=user_id).count()
    return jsonify({"success": True, "count": count})


