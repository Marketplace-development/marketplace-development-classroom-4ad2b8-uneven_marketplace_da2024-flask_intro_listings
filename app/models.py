from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin

db = SQLAlchemy()


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)  # Nieuw veld
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(15), nullable=True)
    address = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    user_rating = db.Column(db.Float, default=5.0)

    # Relationships to listings
    listings_posted = db.relationship(
        'Listing', 
        back_populates='leaver', 
        foreign_keys='Listing.leaver_id'
    )
    listings_responded = db.relationship(
        'Listing', 
        back_populates='sitter', 
        foreign_keys='Listing.sitter_id'
    )
    notifications = db.relationship('Notification', back_populates='user')


    def __repr__(self):
        return f"<User {self.username}>"
    
    # Add the get_id method
    def get_id(self):
        return str(self.id)


class Listing(db.Model):
    __tablename__ = 'listings'  # Naam van de tabel in de database

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False, default='New Plant')
    picture = db.Column(db.String(100), nullable=False, default='Default.png')
    base_price = db.Column(db.Float, nullable=False)  # Geafficheerde prijs
    specie = db.Column(db.String(20), nullable=False)
    light = db.Column(db.Integer, nullable=False)  # Aantal uren licht per dag (bijv. 0-24)
    water = db.Column(db.Float, nullable=False)  # Aantal liter water per dag
    nutrient = db.Column(db.String(20), nullable=False, default='None')  # Meststof- of mineraalbehoefte
    pruning = db.Column(db.String(20), nullable=False, default='None')  # Snoeibehoefte
    sensitivity = db.Column(db.String(100), nullable=True)  # Eventuele gevoeligheid (bv. koud, droogte)
    start_date = db.Column(db.DateTime, nullable=False)  # Begindatum van de periode
    end_date = db.Column(db.DateTime, nullable=False)  # Einddatum van de periode
    
    address = db.Column(db.String(200), nullable=True)
    latitude = db.Column(db.Float, nullable=True)  # Nieuwe veld voor breedtegraad
    longitude = db.Column(db.Float, nullable=True) 


    # Verwijzingen naar de gebruikers (leaver en sitter)
    leaver_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    sitter_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="SET NULL"), nullable=True)

    # Relaties naar de User tabel
    leaver = db.relationship(
    'User',
    back_populates='listings_posted',
    primaryjoin='User.id == Listing.leaver_id'
)
    sitter = db.relationship(
    'User',
    back_populates='listings_responded',
    primaryjoin='User.id == Listing.sitter_id'
)

    def __repr__(self):
        return f"Listing('{self.title}', '{self.specie}', '{self.base_price}')"

class Booking(db.Model):
    __tablename__ = 'bookings'  # Name of the table in the database

    # Primary Key
    id = db.Column(db.Integer, primary_key=True)

    # Foreign Keys
    listing_id = db.Column(db.Integer, db.ForeignKey('listings.id', ondelete="CASCADE"), nullable=False)
    sitter_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="SET NULL"), nullable=True)
    leaver_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    available_period_id = db.Column(db.Integer, nullable=True)  # Placeholder for future AvailablePeriod table
    bid_id = db.Column(db.Integer, nullable=True)  # Placeholder for Bid table

    # Additional Fields
    booked_start_date = db.Column(db.DateTime, nullable=False)
    booked_end_date = db.Column(db.DateTime, nullable=False)
    booking_status = db.Column(db.String(20), nullable=False, default='Pending')  # Status (e.g., Pending, Confirmed)
    booking_price = db.Column(db.Float, nullable=False)

    # Relationships
    listing = db.relationship('Listing', backref='bookings', lazy=True)
    sitter = db.relationship('User', foreign_keys=[sitter_id], backref='accepted_bookings', lazy=True)
    leaver = db.relationship('User', foreign_keys=[leaver_id], backref='created_bookings', lazy=True)

    def __repr__(self):
        return f"Booking('{self.id}', Listing: '{self.listing.title}', Status: '{self.booking_status}', Price: '{self.booking_price}')"

class Favorite(db.Model):
    __tablename__ = 'favorites'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    listing_id = db.Column(db.Integer, db.ForeignKey('listings.id', ondelete="CASCADE"), nullable=False)

    # Relationships
    user = db.relationship('User', backref=db.backref('favorites', lazy='dynamic', cascade="all, delete"))
    listing = db.relationship('Listing', backref=db.backref('favorites', lazy='dynamic', cascade="all, delete"))


    def __repr__(self):
        return f"Favorite(user_id={self.user_id}, listing_id={self.listing_id})"
    

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)
    listing_id = db.Column(db.Integer, db.ForeignKey('listings.id', ondelete="CASCADE"), nullable=True)

    user = db.relationship('User', back_populates='notifications')
    listing = db.relationship('Listing', backref='notifications', lazy=True)


class Review(db.Model):
    __tablename__ = 'review'

    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.id', ondelete="CASCADE"), nullable=False)
    reviewer_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    reviewee_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    feedback = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Review {self.id}, Reviewer {self.reviewer_id}, Reviewee {self.reviewee_id}>"


class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    listing_id = db.Column(db.Integer, db.ForeignKey('listings.id', ondelete="CASCADE"), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    is_read = db.Column(db.Boolean, nullable=False, default=False)  # Nieuw veld

    sender = db.relationship('User', foreign_keys=[sender_id], backref='sent_messages')
    receiver = db.relationship('User', foreign_keys=[receiver_id], backref='received_messages')
    listing = db.relationship('Listing', backref='messages')

class PriceProposal(db.Model):
    __tablename__ = 'priceproposal'

    id = db.Column(db.Integer, primary_key=True)
    listing_id = db.Column(db.Integer, db.ForeignKey('listings.id', ondelete="CASCADE"), nullable=False)
    proposer_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), nullable=False)

    new_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='Pending')  # Status: Pending, Accepted, Rejected
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    listing = db.relationship('Listing', backref='price_proposals')
    proposer = db.relationship('User', backref='price_proposals')

