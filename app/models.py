from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    # Primary key
    userID = db.Column(db.String, primary_key=True)  # Using `userID` as primary key for consistency with your table

    # User information
    username = db.Column(db.String(80), unique=True, nullable=False)  # Unique username
    firstName = db.Column(db.String, nullable=False)
    lastName = db.Column(db.String, nullable=False)
    birthDate = db.Column(db.Date)
    address = db.Column(db.String)
    city = db.Column(db.String)
    postalCode = db.Column(db.String)
    country = db.Column(db.String)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    phone = db.Column(db.String)
    profilePicture = db.Column(db.String)
    nationality = db.Column(db.String)

    # Booleans for roles
    isProvider = db.Column(db.Boolean, default=False)
    isSearcher = db.Column(db.Boolean, default=False)

    # Metadata
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    listings = db.relationship('Listing', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.email}>'

class Listing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    listing_name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.String, db.ForeignKey('user.userID'), nullable=False)  # ForeignKey matches `userID` in User

    def __repr__(self):
        return f'<Listing {self.listing_name}, ${self.price}>'

