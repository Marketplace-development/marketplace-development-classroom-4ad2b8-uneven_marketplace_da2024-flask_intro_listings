from flask_sqlalchemy import SQLAlchemy
import datetime
from . import db

db = SQLAlchemy()


class Users(db.Model):
    # Primary key
    userid = db.Column(db.String, primary_key=True)  # Using userID as primary key for consistency with your table

    # User information
    firstname = db.Column(db.String, nullable=False)
    lastname = db.Column(db.String, nullable=False)
    birthdate = db.Column(db.Date)
    address = db.Column(db.String)
    city = db.Column(db.String)
    postalcode = db.Column(db.String)
    country = db.Column(db.String)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    phone = db.Column(db.String)
    profilepicture = db.Column(db.String)
    nationality = db.Column(db.String)

    # Booleans for roles
    isprovider = db.Column(db.Boolean, default=False)
    issearcher = db.Column(db.Boolean, default=False)

    # Metadata
    createdat = db.Column(db.DateTime, default=datetime.date)

    # # Relationships
    # listings = db.relationship('Listing', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.email}>'

# class Listing(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     listing_name = db.Column(db.String(100), nullable=False)
#     price = db.Column(db.Float, nullable=False)
#     user_id = db.Column(db.String, db.ForeignKey('user.userID'), nullable=False)  # ForeignKey matches userID in User

#     def __repr__(self):
#         return f'<Listing {self.listing_name}, ${self.price}>'