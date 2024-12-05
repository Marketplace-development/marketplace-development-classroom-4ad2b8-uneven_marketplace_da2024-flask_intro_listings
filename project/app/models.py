from flask_sqlalchemy import SQLAlchemy
import datetime
from . import db


    
class Users(db.Model):
    __tablename__ = 'users'
    # Primary key
    userid = db.Column(db.String, primary_key=True)  # Using userid as primary key for consistency with your table

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
    createdat = db.Column(db.DateTime, default=datetime.datetime.utcnow)

     # Relationships
    digitalgoods = db.relationship('DigitalGoods', backref='user', lazy=True)
    


    def __repr__(self):
        return f'<User {self.email}>'

# class Listing(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     listing_name = db.Column(db.String(100), nullable=False)
#     price = db.Column(db.Float, nullable=False)
#     user_id = db.Column(db.String, db.ForeignKey('user.userid'), nullable=False)  # ForeignKey matches userid in User

#     def __repr__(self):
#         return f'<Listing {self.listing_name}, ${self.price}>'


class DigitalGoods(db.Model):
    __tablename__ = 'digitalgoods'
    
    # Primaire sleutel
    goodid = db.Column(db.String, primary_key=True)
    
    # Eigenschappen van digitale goederen
    titleofitinerary = db.Column(db.String, nullable=False)
    descriptionofitinerary = db.Column(db.TEXT)
    userid = db.Column(db.String, db.ForeignKey('users.userid'), nullable=False)
    price = db.Column(db.Numeric)
    createdat = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f'<DigitalGoods {self.titleofitinerary} - ${self.price}>' 