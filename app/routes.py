import os, requests, logging
from flask import Blueprint, redirect, url_for, render_template, flash, request, current_app, jsonify
from app.forms import LoginForm, RegistrationForm, ListingForm, ReviewForm
from app.models import db, Listing, User, Favorite, Notification, Booking, Review, Message, PriceProposal
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from datetime import datetime
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
from urllib3.exceptions import InsecureRequestWarning
import urllib3
import certifi, ssl
import re
from decimal import Decimal


# Maak een aangepaste SSL-context met de juiste certificaten
ssl_context = ssl.create_default_context(cafile=certifi.where())
geolocator = Nominatim(user_agent="plant_exchange_app", ssl_context=ssl_context)
# Gebruik Nominatim voor geocoding, met een aangepaste SSL context
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE


# Onderdruk SSL-verificatie waarschuwingen
urllib3.disable_warnings(InsecureRequestWarning)
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


main = Blueprint('main', __name__, static_folder='static', template_folder='templates')

@main.route('/')
def base():
    return redirect(url_for('main.login'))


from sqlalchemy import and_
@main.route('/home')
@login_required
def home():
    # Get the selected sort option from the dropdown
    sort_option = request.args.get('sort')
    category_filter = request.args.get('category', 'all')

    # Current date to filter out expired or started listings
    current_date = datetime.utcnow()

    # Fetch listings that are available for booking (not yet booked, not created by the current user, not expired, not started)
    query = Listing.query.filter(
        Listing.leaver_id != current_user.id,  # Exclude listings created by the current user
        Listing.sitter_id == None,  # Only listings that have not been booked yet
        Listing.end_date >= current_date,  # Exclude expired listings
        Listing.start_date >= current_date  # Exclude listings that have already started
    )

    # Apply category filter if selected
    if category_filter and category_filter != "all":
        query = query.filter(Listing.specie == category_filter)

    # Apply sorting based on user selection
    if sort_option == 'price_asc':
        listings = query.order_by(Listing.base_price.asc()).all()
    elif sort_option == 'price_desc':
        listings = query.order_by(Listing.base_price.desc()).all()
    elif sort_option == 'start_date_asc':
        listings = query.order_by(Listing.start_date.asc()).all()
    elif sort_option == 'start_date_desc':
        listings = query.order_by(Listing.start_date.desc()).all()
    else:
        listings = query.all()  # Default: no sorting

    # Real-time notification creation for completed bookings
    completed_bookings = Booking.query.filter(
        ((Booking.sitter_id == current_user.id) | (Booking.leaver_id == current_user.id)),
        Booking.booked_end_date < current_date  # Booking has ended
    ).all()

    for booking in completed_bookings:
        if current_user.id == booking.leaver_id:
            # Notify leaver to review sitter
            notification_message = f"""
                Please write a review for your sitter for Booking #{booking.id}. 
                <a href='{url_for('main.write_review', booking_id=booking.id)}'>Click here to review</a>
            """
            add_notification_if_not_exists(current_user.id, notification_message)

        elif current_user.id == booking.sitter_id:
            # Notify sitter to review leaver
            notification_message = f"""
                Please write a review for the leaver for Booking #{booking.id}. 
                <a href='{url_for('main.write_review', booking_id=booking.id)}'>Click here to review</a>
            """
            add_notification_if_not_exists(current_user.id, notification_message)

    # Fetch unread notifications for the user
    unread_notifications = Notification.query.filter(
        Notification.user_id == current_user.id,
        Notification.is_read == False
    ).count()

    # Fetch unread messages count for the user
    unread_messages_count = Message.query.filter(
        Message.receiver_id == current_user.id,
        Message.is_read == False
    ).count()

    # Render the home page
    return render_template(
        'home.html',
        listings=listings,
        unread_notifications=unread_notifications,
        unread_messages_count=unread_messages_count)


def add_notification_if_not_exists(user_id, message):
    """
    Check if a notification with the same message exists for the user.
    If not, create a new notification.
    """
    existing_notification = Notification.query.filter_by(user_id=user_id, message=message).first()
    if not existing_notification:
        new_notification = Notification(user_id=user_id, message=message, timestamp=datetime.utcnow())
        db.session.add(new_notification)
        db.session.commit()



@main.route('/about')
@login_required
def about():
    return render_template('about.html', title='About')


@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Controleer of gebruikersnaam uniek is
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash("This username is already taken. Please choose a different one.", "error")
            return render_template('register.html', form=form)

        # Maak een nieuwe gebruiker aan
        new_user = User(
            username=form.username.data.strip(),
            first_name=form.first_name.data.strip(),
            last_name=form.last_name.data.strip(),
            email=form.email.data.strip(),
            phone_number=form.phone_number.data.strip(),
            address=f"{form.street.data.strip()} {form.street_number.data.strip()}, {form.postcode.data.strip()} {form.country.data.strip()}"
        )

        try:
            db.session.add(new_user)
            db.session.commit()
            flash("Registration successful! Please log in.", "success")
            return redirect(url_for('main.login'))
        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred: {e}", "error")
    elif form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{field}: {error}", "error")

    return render_template('register.html', form=form)



@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Haal de gebruiker op uit de database
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            # Log de gebruiker in
            login_user(user)
            flash(f"Welcome, {user.username}!", "success")
            return redirect(url_for('main.home'))  # Redirect naar de homepagina na inloggen
        else:
            flash("Invalid username", "error")
    return render_template('login.html', form=form)


@main.route('/account')
@login_required
def account():
    current_date = datetime.utcnow()

    # Fetch ongoing bookings: only include bookings that are confirmed and have not yet ended
    ongoing_bookings = Booking.query.filter(
        Booking.sitter_id != None,
        Booking.leaver_id == current_user.id,
        Booking.booked_start_date < current_date,
        Booking.booked_end_date >= current_date  # End date is in the future
    ).all()

    # Fetch completed bookings: bookings where the end date is in the past
    completed_bookings = Booking.query.filter(
        Booking.leaver_id == current_user.id,
        Booking.sitter_id != None,
        Booking.booked_end_date < current_date  # End date is in the past
    ).all()

    # Get listings that have never been booked and have expired
    never_booked_listings = get_never_booked_listings(current_user)

    # Fetch listings created by the user that have been booked by others
    my_booked_listings = Listing.query.filter(
        Listing.leaver_id == current_user.id,
        Listing.sitter_id != None  # Listings with a sitter assigned
    ).all()

    # Fetch active listings posted by the user that have not been booked and have not expired
    my_listings = Listing.query.filter(
        Listing.leaver_id == current_user.id,
        Listing.sitter_id == None,  # Listings that are not booked
        Listing.end_date >= current_date  # Listings that have not expired
    ).all()

    # Calculate badges dynamically for the logged-in user
    badges = calculate_badges(current_user)

    # Render the account page with bookings, listings, and badges
    return render_template(
        'account.html',
        ongoing_bookings=ongoing_bookings,
        completed_bookings=completed_bookings,
        never_booked_listings=never_booked_listings,
        my_booked_listings=my_booked_listings,
        my_listings=my_listings,
        badges=badges
    )


# Helper functie voor account routing
def get_never_booked_listings(user):
    """Get listings that have expired without being booked."""
    current_date = datetime.utcnow()
    never_booked_listings = Listing.query.filter(
        Listing.leaver_id == user.id,
        Listing.sitter_id == None,  # No sitter assigned, meaning not booked
        Listing.start_date < current_date  # Start date has passed
    ).all()
    return never_booked_listings


@main.route('/logout', methods=['GET'])
def logout():
    logout_user()  # Dit logt de gebruiker uit
    flash("You have been logged out.", "success")
    return redirect(url_for('main.login'))


@main.route('/create_listing', methods=['GET', 'POST'])
@login_required
def create_listing():
    form = ListingForm()

    if form.validate_on_submit():
        try:
            # Validate price input
            base_price = form.base_price.data
            if not base_price or not str(base_price).replace('.', '', 1).isdigit():
                form.base_price.errors.append("Price must be a valid number with two decimal places.")
                return render_template('create_listing.html', form=form)

            base_price = float(base_price)

            # Validate water input
            water = form.water.data
            if not water or not str(water).replace('.', '', 1).isdigit():
                form.water.errors.append("Water must be a valid number with two decimal places.")
                return render_template('create_listing.html', form=form)

            water = float(water)

            # Ensure the start date is before the end date
            if form.start_date.data >= form.end_date.data:
                flash("End date must be after the start date.", "danger")
                return render_template('create_listing.html', form=form)

            # Handle picture upload
            picture_file = form.picture.data
            if picture_file and picture_file.filename:
                filename = secure_filename(picture_file.filename)
                picture_path = os.path.join(current_app.root_path, 'static/uploads', filename)
                picture_file.save(picture_path)  # Save the uploaded file
            else:
                filename = "Default.png"  # Use a default image if no file is uploaded

             # Combine address fields into a full address
            street = form.street.data
            street_number = form.street_number.data
            city = form.city.data
            postcode = form.postcode.data
            country = form.country.data
            full_address = f"{street} {street_number}, {postcode} {city}, {country}"

            location = geolocator.geocode(full_address)
            if location:
                latitude = location.latitude
                longitude = location.longitude
                print(f"Geocoded latitude: {latitude}, longitude: {longitude}")
            else:
                print("Geocoding failed for address:", full_address)  # Debug print voor falen
                flash("The address you submitted could not be found. Please try again.", "danger")
                return render_template('create_listing.html', form=form)

            # Create a new listing
            listing = Listing(
                title=form.title.data,
                picture=filename,  # Save only the filename
                base_price=base_price,
                specie=form.specie.data,
                light=form.light.data,
                water=water,
                nutrient=form.nutrient.data,
                pruning=form.pruning.data,
                sensitivity=form.sensitivity.data,
                start_date=form.start_date.data,
                end_date=form.end_date.data,
                address=full_address,
                latitude=form.latitude.data,
                longitude=form.longitude.data,
                leaver_id=current_user.id,  # Associate with the logged-in user
            )

            # Save to the database
            db.session.add(listing)
            db.session.commit()
            print(f"Listing opgeslagen met latitude: {listing.latitude}, longitude: {listing.longitude}")
            flash("Listing added to your account.", "success")
            return redirect(url_for('main.account'))

        except ValueError as e:
            flash(f"Error in processing data: {str(e)}", "danger")
        except Exception as e:
            db.session.rollback()
            flash(f"An unexpected error occurred: {str(e)}", "danger")

    elif request.method == 'POST':
        flash("There were errors in your form submission. Please check the fields and try again.", "danger")

    return render_template('create_listing.html', form=form)


@main.route('/confirm_delete_listing/<int:listing_id>', methods=['GET', 'POST'])
@login_required
def confirm_delete_listing(listing_id):
    listing = Listing.query.get_or_404(listing_id)
    try:
        db.session.delete(listing)
        db.session.commit()
        flash("Listing deleted successfully.", "success")
        return redirect(url_for('main.account'))
    except Exception as e:
        db.session.rollback()
        flash(f"Error deleting listing: {e}", "error")
    return render_template('account.html', listing=listing)



@main.route('/view_listing/<int:listing_id>', methods=['GET'])
@login_required
def view_listing(listing_id):
    listing = Listing.query.get_or_404(listing_id)
    price_range_min = listing.base_price - 3
    price_range_max = listing.base_price + 3

    similar_listings = Listing.query.filter(
        Listing.id != listing.id,  # Exclude current listing
        Listing.specie == listing.specie,  # Same category
        and_(
            Listing.base_price >= price_range_min,
            Listing.base_price <= price_range_max
        )
    ).limit(3).all()  # Limit to 4 similar listings

    return render_template(
        'view_listing.html',
        listing=listing,
        similar_listings=similar_listings
    )


@main.route('/search', methods=['GET'])
@login_required
def search():
    query = request.args.get('query', '').strip()  # Get the search term
    search_type = request.args.get('type', 'users')  # Default to searching users

    if search_type == 'users':
        # Search users by username
        results = User.query.filter(User.username.ilike(f'%{query}%')).all() if query else []

        # Ensure all user ratings have a default value of 5 if None
        for user in results:
            if user.user_rating is None:
                user.user_rating = 5

        return render_template('search_results.html',
                               user_results=results,
                               plant_results=[],
                               query=query,
                               search_type=search_type)

    elif search_type == 'plants':
        current_date = datetime.utcnow()

        # Search for available listings
        results = Listing.query.filter(
            (Listing.title.ilike(f'%{query}%')) | (Listing.specie.ilike(f'%{query}%'))
        ).filter(
            Listing.sitter_id == None,  # Exclude listings with assigned sitter (booked)
            Listing.end_date >= current_date,  # Exclude expired listings
            Listing.leaver_id != current_user.id  # Exclude listings of the current user
        ).all() if query else []

        return render_template('search_results.html',
                               user_results=[],
                               plant_results=results,
                               query=query,
                               search_type=search_type)


@main.route('/profile/<int:user_id>', methods=['GET'])
@login_required
def profile(user_id):
    # Fetch user details by user ID
    user = User.query.get_or_404(user_id)

    # Set default rating to 5 if None
    if user.user_rating is None:
        user.user_rating = 5

    # Fetch active plant listings created by the user that have not been booked and are not expired
    current_date = datetime.utcnow()
    plant_listings = Listing.query.filter(
        Listing.leaver_id == user.id,
        Listing.sitter_id == None,  # Listings that have not been booked
        Listing.end_date >= current_date  # Listings that have not expired
    ).all()

    # Calculate badges dynamically
    badges = calculate_badges(user)

    # Fetch reviews written about this user
    reviews = Review.query.filter_by(reviewee_id=user.id).all()

    # Render the profile page with user, their listings, badges, and reviews
    return render_template('profile.html', user=user, plant_listings=plant_listings, badges=badges, reviews=reviews)


@main.route('/care_for_plant/<int:listing_id>', methods=['GET', 'POST'])
@login_required
def care_for_plant(listing_id):
    listing = Listing.query.get_or_404(listing_id)
    # Add logic for "taking care of the plant" (e.g., assigning sitter_id)
    return redirect(url_for('main.view_listing', listing_id=listing.id))


@main.route('/listing/<int:listing_id>/booking', methods=['GET', 'POST'])
@login_required
def booking(listing_id):
    listing = Listing.query.get_or_404(listing_id)

    # Prevent booking if the listing has already been booked
    if listing.sitter_id is not None:
        flash('This plant has already been booked.')
        return redirect(url_for('main.home'))

    # Prevent the listing owner from booking their own plant
    if current_user.id == listing.leaver_id:
        flash('You cannot book your own listing.')
        return redirect(url_for('main.view_listing', listing_id=listing_id))

    if request.method == 'POST':
        # Update the listing to indicate that it is booked
        listing.sitter_id = current_user.id  # Set the current user as the sitter

        # Create a new booking record
        new_booking = Booking(
            listing_id=listing.id,
            sitter_id=current_user.id,
            leaver_id=listing.leaver_id,
            booked_start_date=listing.start_date,
            booked_end_date=listing.end_date,
            booking_status='Confirmed',
            booking_price=listing.base_price
        )

        # Create a notification for the listing owner
        notification_message = f"Your plant '{listing.title}' has been booked by {current_user.username}."
        new_notification = Notification(
            user_id=listing.leaver_id,
            message=notification_message
        )

        try:
            # Add the booking and the notification to the database
            db.session.add(new_booking)
            db.session.add(new_notification)
            db.session.commit()

            flash('You have successfully booked this plant.')
            return redirect(url_for('main.account'))

        except Exception as e:
            db.session.rollback()
            flash('An error occurred while booking the plant. Please try again later.')
            return redirect(url_for('main.view_listing', listing_id=listing_id))

    return render_template('booking.html', listing=listing)


@main.route('/chat_between_customers/<int:listing_id>', methods=['GET', 'POST'])
@login_required
def chat_between_customers(listing_id):
    listing = Listing.query.get_or_404(listing_id)

    # Ontvanger bepalen
    if current_user.id == listing.leaver.id:
        receiver_id = request.args.get('receiver_id', type=int)
        if not receiver_id:

            # Redirect naar dezelfde chat pagina met een foutmelding
            messages = Message.query.filter(
                (Message.listing_id == listing_id) &
                ((Message.sender_id == current_user.id) | (Message.receiver_id == current_user.id))
            ).order_by(Message.timestamp.asc()).all()
            return render_template('chat_between_customers.html', listing=listing, messages=messages)
    else:
        receiver_id = listing.leaver.id

    # Berichten ophalen
    messages = Message.query.filter(
        (Message.listing_id == listing_id) &
        ((Message.sender_id == current_user.id) | (Message.receiver_id == current_user.id))
    ).order_by(Message.timestamp.asc()).all()

    # Berichten verwerken bij POST
    if request.method == 'POST':
        message_content = request.form.get('message')
        if not message_content:
            flash("Message content cannot be empty.", "error")
            return render_template('chat_between_customers.html', listing=listing, messages=messages)

        # Nieuw bericht aanmaken
        new_message = Message(
            sender_id=current_user.id,
            receiver_id=receiver_id,
            listing_id=listing_id,
            content=message_content,
            timestamp=datetime.utcnow(),
            is_read=False
        )
        db.session.add(new_message)
        db.session.commit()
        flash('Message sent successfully!', 'success')
        return redirect(url_for('main.chat_between_customers', listing_id=listing_id))

    return render_template('chat_between_customers.html', listing=listing, messages=messages)




@main.route('/favorites')
@login_required
def favorites():
    # Current date to filter out expired listings
    current_date = datetime.utcnow()

    # Query to fetch favorite listings of the current user that are active and not booked
    favorite_listings = Listing.query.join(
        Favorite, Favorite.listing_id == Listing.id
    ).filter(
        Favorite.user_id == current_user.id,
        Listing.sitter_id == None,  # Not booked
        Listing.end_date >= current_date  # Not expired
    ).all()

    return render_template('favorites.html', favorite_listings=favorite_listings)



@main.route('/add_favorite/<int:listing_id>', methods=['POST'])
@login_required
def add_favorite(listing_id):
    # Ensure the listing exists
    listing = db.session.get(Listing, listing_id)
    if not listing:
        flash("Listing not found.", "danger")
        return redirect(url_for('main.home'))

    # Check if the favorite already exists
    existing_favorite = Favorite.query.filter_by(user_id=current_user.id, listing_id=listing_id).first()

    if existing_favorite:
        # Remove the favorite if it exists
        db.session.delete(existing_favorite)
        flash('Removed from favorites.', 'info')
    else:
        # Add the favorite if it doesn't exist
        new_favorite = Favorite(user_id=current_user.id, listing_id=listing_id)
        db.session.add(new_favorite)
        flash('Added to favorites.', 'success')

        # add notification
        notification_message = f"{current_user.username} added your plant to favorites!"
        notification = Notification(
            user_id=listing.leaver_id,
            message=notification_message,
            listing_id=listing.id
        )
        db.session.add(notification)

    # Commit changes to the database
    db.session.commit()
    return redirect(url_for('main.home'))


@main.route('/remove_favorite/<int:listing_id>', methods=['POST'])
@login_required
def remove_favorite(listing_id):
    # Fetch the favorite based on user_id and listing_id
    favorite = Favorite.query.filter_by(user_id=current_user.id, listing_id=listing_id).first()
    if favorite:
        db.session.delete(favorite)
        db.session.commit()
        flash('Favorite removed successfully.', 'info')
    else:
        flash('Favorite not found.', 'danger')

    return redirect(url_for('main.favorites'))

@main.route('/edit_listing/<int:listing_id>', methods=['GET', 'POST'])
@login_required
def edit_listing(listing_id):
    listing = Listing.query.get_or_404(listing_id)
    
    if request.method == 'POST':
        # Haal de waarden van het formulier op
        listing.title = request.form['title']
        listing.base_price = request.form['price']
        listing.specie = request.form['specie']
        listing.light = request.form['light']
        listing.water = request.form['water']

        # Haal de nieuwe latitude en longitude op
        listing.address = request.form['address']

        # Geocoding van het adres
        try:
            location = geolocator.geocode(listing.address)
            if location:
                listing.latitude = location.latitude
                listing.longitude = location.longitude
                print(f"Geocoded latitude: {listing.latitude}, longitude: {listing.longitude}")
            else:
                print("Geocoding returned no location for address:", listing.address)
                flash("Het ingevoerde adres kon niet worden gevonden. Controleer het adres en probeer opnieuw.", "danger")
                return redirect(url_for('main.edit_listing', listing_id=listing_id))
        except Exception as e:
            flash(f"Fout bij geocodering: {e}", "danger")
            return redirect(url_for('main.edit_listing', listing_id=listing_id))
                            

        # Verwerk de nieuwe afbeelding (indien geüpload)
        picture_file = request.files.get('picture')
        if picture_file and picture_file.filename != '':
            try:
                filename = secure_filename(picture_file.filename)
                upload_folder = os.path.join(current_app.root_path, 'static/uploads')

                # Controleer of de directory bestaat, zo niet, maak deze aan
                if not os.path.exists(upload_folder):
                    os.makedirs(upload_folder)  # Maakt de 'uploads' map aan indien niet bestaand

                picture_path = os.path.join(upload_folder, filename)
                picture_file.save(picture_path)
                listing.picture = filename
            except Exception as e:
                flash(f"Er is een fout opgetreden bij het uploaden van de afbeelding: {e}", "danger")
                return redirect(url_for('main.edit_listing', listing_id=listing_id))

        # Probeer de wijzigingen op te slaan in de database
        try:
            db.session.commit()
            flash("De plantgegevens zijn bijgewerkt.", "success")
            return redirect(url_for('main.view_listing', listing_id=listing_id))
        except Exception as e:
            db.session.rollback()
            flash(f"Er is een fout opgetreden bij het bijwerken van de plant: {e}", "danger")
            return redirect(url_for('main.edit_listing', listing_id=listing_id))

    # Als het geen POST-verzoek is, geef dan de bewerkpagina weer met de huidige waarden van de plant
    return render_template('edit_listing.html', listing=listing)

@main.route('/notifications')
@login_required
def notifications():
    notifications = Notification.query.filter_by(user_id=current_user.id).order_by(Notification.timestamp.desc()).all()
    valid_notifications = [n for n in notifications if n.listing]  # Filter notificaties met een geldige listing

    return render_template('notifications.html', notifications=notifications)

@main.route('/mark_notification_read/<int:notification_id>', methods=['POST'])
@login_required
def mark_notification_read(notification_id):
    notification = Notification.query.get_or_404(notification_id)
    if notification.user_id != current_user.id:
        flash("You are not authorized to mark this notification as read.", "danger")
        return redirect(url_for('main.notifications'))

    notification.is_read = True
    db.session.commit()
    return redirect(url_for('main.notifications'))

@main.route('/booking/<int:booking_id>/review', methods=['GET', 'POST'])
@login_required
def write_review(booking_id):
    booking = Booking.query.get_or_404(booking_id)

    # Ensure the current user is either the leaver or sitter in the booking
    if current_user.id not in [booking.leaver_id, booking.sitter_id]:
        flash('You are not authorized to review this booking.', 'danger')
        return redirect(url_for('main.home'))

    # Check if the booking has ended
    if booking.booked_end_date >= datetime.utcnow():
        flash('You can only write a review after the booking has ended.', 'danger')
        return redirect(url_for('main.account'))

    # Prevent duplicate reviews for the same user in the same booking
    existing_review = Review.query.filter_by(
        booking_id=booking.id,
        reviewer_id=current_user.id
    ).first()
    if existing_review:
        flash('You have already reviewed this booking.', 'info')
        return redirect(url_for('main.account'))

    # Identify the reviewee
    reviewee_id = booking.sitter_id if current_user.id == booking.leaver_id else booking.leaver_id

    form = ReviewForm()
    if form.validate_on_submit():
        # Create a new review
        new_review = Review(
            booking_id=booking.id,
            reviewer_id=current_user.id,
            reviewee_id=reviewee_id,
            rating=form.rating.data,
            feedback=form.feedback.data,
            created_at=datetime.utcnow()
        )
        db.session.add(new_review)

        # Update the reviewee's user rating
        update_user_rating(reviewee_id)

        db.session.commit()
        flash('Review submitted successfully and user rating updated.', 'success')
        return redirect(url_for('main.account'))

    return render_template('write_review.html', form=form, booking=booking)

def update_user_rating(user_id):
    """
    Recalculate the average rating for a user and update their user_rating field.
    If there are no reviews, set the user_rating to 5 by default.
    """
    user = User.query.get(user_id)
    if not user:
        return

    # Fetch all reviews where the user is the reviewee
    reviews = Review.query.filter_by(reviewee_id=user_id).all()
    if reviews:
        # Calculate the average rating
        total_rating = sum(review.rating for review in reviews)
        average_rating = total_rating / len(reviews)
        user.user_rating = round(average_rating, 2)  # Update the user_rating field
    else:
        # No reviews, set rating to 5
        user.user_rating = 5

    print(f"Updated user {user_id} rating to: {user.user_rating}")  # Debugging
    db.session.commit()


@main.route('/user/<int:user_id>/reviews', methods=['GET'])
@login_required
def user_reviews(user_id):
    # Fetch the user by their ID
    user = User.query.get_or_404(user_id)

    # Fetch reviews where this user is the reviewee
    reviews = Review.query.filter_by(reviewee_id=user.id).all()

    # Debugging to confirm data retrieval
    print(f"User: {user.username}")
    print(f"Reviews Retrieved: {len(reviews)}")
    for review in reviews:
        print(f"Review ID: {review.id}, Reviewer ID: {review.reviewer_id}, Rating: {review.rating}")

    # Pass data to the template
    return render_template('user_reviews.html', user=user, reviews=reviews)

def calculate_badges(user):
    badges = []

    # Badge 1: "Cactus Whisperer" for sitting a cactus
    cactus_sittings = Booking.query.join(Listing).filter(
        Booking.sitter_id == user.id,
        Listing.specie.ilike('%cactus%')
    ).count()
    if cactus_sittings > 0:
        badges.append("Cactus Whisperer")

    # Badge 2: "Green Thumb Guru" for maintaining a 5-star rating
    if user.user_rating == 5:
        badges.append("Green Thumb Guru")

    # Badge 3: "Plant Protector" for completing more than 10 bookings
    completed_bookings = Booking.query.filter(
        ((Booking.sitter_id == user.id) | (Booking.leaver_id == user.id)),
        Booking.booking_status == 'Completed'
    ).count()
    if completed_bookings > 10:
        badges.append("Plant Protector")

    # Badge 4: "Rare Plant Enthusiast" for hosting rare plants
    rare_plants = Listing.query.filter(
        Listing.leaver_id == user.id,
        Listing.specie.ilike('%orchid%') | Listing.specie.ilike('%bonsai%')
    ).count()
    if rare_plants > 0:
        badges.append("Rare Plant Enthusiast")

    # Badge 5: "Eco-Friendly Gardener" for caring for low-maintenance plants
    eco_friendly_plants = Listing.query.filter(
        Listing.sitter_id == user.id,
        Listing.water <= 1.0,  # Low water requirements
        Listing.light <= 6  # Low light requirements
    ).count()
    if eco_friendly_plants > 0:
        badges.append("Eco-Friendly Gardener")

    # Badge 6: "Helping Hand" for completing first booking
    if completed_bookings >= 1:
        badges.append("Helping Hand")

    # Badge 7: "Trusted Companion" for receiving 10 or more 5-star reviews
    five_star_reviews = Review.query.filter(
        Review.reviewee_id == user.id,
        Review.rating == 5
    ).count()
    if five_star_reviews >= 10:
        badges.append("Trusted Companion")

    # Badge 8: "Community Builder" for hosting or sitting plants for 5+ unique users
    unique_users = Booking.query.filter(
        ((Booking.sitter_id == user.id) | (Booking.leaver_id == user.id))
    ).distinct(Booking.leaver_id if Booking.sitter_id == user.id else Booking.sitter_id).count()
    if unique_users >= 5:
        badges.append("Community Builder")

    return badges


def calculate_leaderboard():
    """
    A simple leaderboard based on the number of reviews and average ratings.
    """
    users = User.query.all()  # Fetch all users
    leaderboard = []

    for user in users:
        # Calculate total reviews and average rating
        reviews = Review.query.filter_by(reviewee_id=user.id).all()
        total_reviews = len(reviews)
        if total_reviews > 0:
            average_rating = sum(review.rating for review in reviews) / total_reviews
        else:
            average_rating = 0  # Default if no reviews

        # Leaderboard entry
        leaderboard.append({
            'username': user.username,
            'total_reviews': total_reviews,
            'average_rating': round(average_rating, 2),
        })

    # Sort leaderboard by average rating, then by total reviews
    leaderboard.sort(key=lambda x: (x['average_rating'], x['total_reviews']), reverse=True)

    return leaderboard


@main.route('/leaderboard')
@login_required
def leaderboard():
    leaderboard_data = calculate_leaderboard()
    return render_template('leaderboard.html', leaderboard=leaderboard_data)

@main.route('/api/listings', methods=['GET'])
@login_required
def api_listings():
    # Haal alle listings op behalve die van de ingelogde gebruiker
    listings = Listing.query.filter(Listing.leaver_id != current_user.id).all()
    listings_data = []
    for listing in listings:
        listings_data.append({
            'id': listing.id,
            'title': listing.title,
            'latitude': listing.latitude,
            'longitude': listing.longitude,
            'base_price': listing.base_price,
            'specie': listing.specie,
            'view_url': url_for('main.view_listing', listing_id=listing.id)  # URL naar de view_listing pagina
        })
    
    return jsonify(listings_data)


@main.route('/propose_price/<int:listing_id>', methods=['POST'])
@login_required
def propose_price(listing_id):
    listing = Listing.query.get_or_404(listing_id)
    new_price = request.form.get('new_price')

    # Regular expression om een prijs te controleren met twee decimalen
    price_pattern = r'^\d+(\.\d{2})?$'

    if not new_price or not re.match(price_pattern, new_price):
        flash('Please enter a valid price in the format 9.00.')
        return redirect(url_for('main.view_listing', listing_id=listing_id))

    # Omzetten van de prijs naar een float met twee decimalen
    try:
        new_price = Decimal(new_price).quantize(Decimal('0.00'))
    except:
        flash('Invalid price format. Please enter a valid price.')
        return redirect(url_for('main.view_listing', listing_id=listing_id))

    # Maak het prijsvoorstel aan
    price_proposal = PriceProposal(
        listing_id=listing_id,
        proposer_id=current_user.id,
        new_price=new_price
    )
    db.session.add(price_proposal)
    db.session.commit()

    # **Notificatie naar de eigenaar van de listing**
    # Hier sturen we de notificatie naar de eigenaar van de listing (leaver_id)
    notification_message_owner = f"{current_user.username} has proposed a new price for your plant '{listing.title}': €{new_price:.2f}"
    notification_owner = Notification(
        user_id=listing.leaver_id,  # Stuur naar de eigenaar
        message=notification_message_owner,
        listing_id=listing.id
    )
    db.session.add(notification_owner)

    # **Notificatie naar de persoon die het voorstel heeft gedaan (Sitter)**
    # Hier sturen we de notificatie naar de bieder (proposer_id)
    notification_message_proposer = f"Your price proposal for '{listing.title}' has been successfully sent."
    notification_proposer = Notification(
        user_id=current_user.id,  # Stuur naar degene die het voorstel heeft gedaan
        message=notification_message_proposer,
        listing_id=listing.id
    )
    db.session.add(notification_proposer)

    db.session.commit()

    flash("Your price proposal has been sent.", category='danger')

    return render_template('booking.html', listing=listing)

@main.route('/answer-notification/<int:notification_id>', methods=['POST'])
@login_required
def answer_notification(notification_id):
    # Haal de notificatie op
    notification = Notification.query.get_or_404(notification_id)

    # Controleer of de notificatie van de huidige gebruiker is
    if notification.user_id != current_user.id:
        flash("You are not authorized to answer this notification.")
        return redirect(url_for('main.notifications'))

    # Markeer notificatie als gelezen
    notification.is_read = True
    db.session.commit()

    # Haal de gekoppelde listing op
    listing = Listing.query.get(notification.listing_id)
    if not listing:
        flash("The associated listing could not be found.")
        return redirect(url_for('main.notifications'))

    # Haal het meest recente prijsvoorstel op
    price_proposal = PriceProposal.query.filter_by(listing_id=listing.id).order_by(PriceProposal.id.desc()).first()

    if not price_proposal:
        flash("No price proposal found for this listing.")
        return redirect(url_for('main.notifications'))

    # Render de pagina met de juiste gegevens, inclusief het prijsvoorstel
    return render_template(
        'answer_notification.html',
        notification=notification,
        listing=listing,
        price_proposal=price_proposal
    )


@main.route('/notifications')
@login_required
def price_notifications():
    user_notifications = Notification.query.filter_by(user_id=current_user.id).all()
    return render_template('notifications.html', notifications=user_notifications)

# Route om de originele prijs goed te keuren
@main.route('/approve-price/<int:listing_id>', methods=['POST'])
@login_required
def approve_price(listing_id):
    listing = Listing.query.get_or_404(listing_id)

    # Controleer of de huidige gebruiker de eigenaar is
    if listing.leaver_id != current_user.id:
        flash("You are not authorized to approve this price.")
        return redirect(url_for('main.notifications'))

    # Haal het prijsvoorstel op
    price_proposal = PriceProposal.query.filter_by(listing_id=listing_id).first()
    if not price_proposal:
        flash("No price proposal found.")
        return redirect(url_for('main.notifications'))

    # Maak de booking aan
    new_booking = Booking(
        listing_id=listing_id,
        sitter_id=price_proposal.proposer_id,
        leaver_id=listing.leaver_id,
        booked_start_date=listing.start_date,
        booked_end_date=listing.end_date,
        booking_status='Confirmed',
        booking_price=price_proposal.new_price
    )
    db.session.add(new_booking)

    # Verwijder het prijsvoorstel
    db.session.delete(price_proposal)
    db.session.commit()

    # Notificatie naar de Sitter (voorstel is goedgekeurd)
    notification_message = f"Your price proposal for '{listing.title}' has been approved and the plant has been booked!"
    notification_sitter = Notification(
        user_id=price_proposal.proposer_id,
        message=notification_message,
        listing_id=listing.id
    )
    db.session.add(notification_sitter)

    db.session.commit()

    flash('You have approved the price and the booking is confirmed.')
    return redirect(url_for('main.notifications'))

@main.route('/reject-price/<int:listing_id>', methods=['POST'])
@login_required
def reject_price(listing_id):
    listing = Listing.query.get_or_404(listing_id)

    # Controleer of de huidige gebruiker de eigenaar is
    if listing.leaver_id != current_user.id:
        flash("You are not authorized to reject this price.")
        return redirect(url_for('main.notifications'))

    # Haal het prijsvoorstel op
    price_proposal = PriceProposal.query.filter_by(listing_id=listing_id).first()
    if not price_proposal:
        flash("No price proposal found.")
        return redirect(url_for('main.notifications'))

    # Verwijder het prijsvoorstel (afwijzen)
    db.session.delete(price_proposal)
    db.session.commit()

    # Notificatie naar de Sitter (voorstel is afgewezen)
    notification_message = f"Your price proposal for '{listing.title}' has been rejected."
    notification_sitter = Notification(
        user_id=price_proposal.proposer_id,
        message=notification_message,
        listing_id=listing.id
    )
    db.session.add(notification_sitter)

    db.session.commit()

    flash('You have rejected the price proposal.')
    return redirect(url_for('main.notifications'))


@main.route('/messages')
@login_required
def messages():
    """
    Route to display all messages received by the current user.
    Messages will be grouped by the sender and their associated listing.
    """
    # Fetch all received messages ordered by timestamp
    messages = Message.query.filter_by(receiver_id=current_user.id).order_by(Message.timestamp.desc()).all()

    # Mark unread messages as read
    unread_messages = Message.query.filter_by(receiver_id=current_user.id, is_read=False).all()
    for message in unread_messages:
        message.is_read = True
    db.session.commit()

    return render_template('messages.html', messages=messages)

