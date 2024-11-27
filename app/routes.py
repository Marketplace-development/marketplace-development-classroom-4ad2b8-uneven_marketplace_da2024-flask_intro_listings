from flask import Blueprint, request, redirect, url_for, render_template, session, flash
from werkzeug.security import generate_password_hash
from .models import db, User, Listing

main = Blueprint('main', __name__)

# Home route
@main.route('/')
def index():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        listings = Listing.query.filter_by(user_id=user.userID).all()  # Fetch listings for logged-in user
        return render_template('index.html', username=user.username, listings=listings)
    return render_template('index.html', username=None)

# Register route
@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Collect form data
        data = {
            'username': request.form['username'],
            'firstName': request.form['firstName'],
            'lastName': request.form['lastName'],
            'birthDate': request.form['birthDate'],
            'address': request.form['address'],
            'city': request.form['city'],
            'postalCode': request.form['postalCode'],
            'country': request.form['country'],
            'email': request.form['email'],
            'password': generate_password_hash(request.form['password']),  # Hash the password
            'phone': request.form.get('phone'),
            'profilePicture': request.form.get('profilePicture'),
            'nationality': request.form.get('nationality'),
            'isProvider': 'isProvider' in request.form,  # Checkbox
            'isSearcher': 'isSearcher' in request.form  # Checkbox
        }

        # Check if username or email already exists
        if User.query.filter_by(username=data['username']).first() or User.query.filter_by(email=data['email']).first():
            flash("Username or email is already registered.")
            return redirect(url_for('main.register'))

        # Create new user
        new_user = User(**data)
        db.session.add(new_user)
        db.session.commit()

        # Log the user in
        session['user_id'] = new_user.userID
        flash("Registration successful!")
        return redirect(url_for('main.index'))

    return render_template('register.html')

# Login route
@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        user = User.query.filter_by(username=username).first()
        if user:
            session['user_id'] = user.userID
            flash("Login successful!")
            return redirect(url_for('main.index'))
        flash("User not found.")
        return redirect(url_for('main.login'))

    return render_template('login.html')

# Logout route
@main.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    flash("You have been logged out.")
    return redirect(url_for('main.index'))

# Add listing route
@main.route('/add-listing', methods=['GET', 'POST'])
def add_listing():
    if 'user_id' not in session:
        flash("You need to log in to add a listing.")
        return redirect(url_for('main.login'))
    
    if request.method == 'POST':
        listing_name = request.form['listing_name']
        price = float(request.form['price'])
        new_listing = Listing(listing_name=listing_name, price=price, user_id=session['user_id'])
        db.session.add(new_listing)
        db.session.commit()
        flash("Listing added successfully!")
        return redirect(url_for('main.listings'))

    return render_template('add_listing.html')

# Listings route
@main.route('/listings')
def listings():
    all_listings = Listing.query.all()
    return render_template('listings.html', listings=all_listings)

