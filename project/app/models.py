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
    birthdate = db.Column(db.Date, default="")
    address = db.Column(db.String, default="")
    city = db.Column(db.String, default="")
    postalcode = db.Column(db.String, default="")
    country = db.Column(db.String, default="")
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, default="")
    profilepicture = db.Column(db.String, default="")
    nationality = db.Column(db.String, default="")

    # Booleans for roles
    isprovider = db.Column(db.Boolean, default=False)
    issearcher = db.Column(db.Boolean, default=False)

    # Metadata
    createdat = db.Column(db.DateTime, default=datetime.datetime.utcnow)

     # Relationships
    digitalgoods = db.relationship('DigitalGoods', backref='user', lazy=True)
    
    def check_password(self, password):
        return self.password == password

    def set_password(self, password):
        self.password = password

    def __repr__(self):
        return f'<User {self.email}>'

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
    pdf_url = db.Column(db.String(1024), nullable=False)

    def __repr__(self):
        return f'<DigitalGoods {self.titleofitinerary} - ${self.price}>' 
    

class Gekocht(db.Model):
    __tablename__ = 'gekocht'

    # Primaire sleutel
    gekochtid = db.Column(db.String, primary_key=True)

    # Foreign keys
    userid = db.Column(db.String, db.ForeignKey('users.userid'), nullable=False)  # Verwijst naar Users.userid
    goodid = db.Column(db.String, db.ForeignKey('digitalgoods.goodid'), nullable=False)  # Verwijst naar DigitalGoods.goodid

    # Metadata
    createdat = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    # Relaties
    user = db.relationship('Users', backref='gekochte_reizen', lazy=True)  # Relatie naar Users
    good = db.relationship('DigitalGoods', backref='gekocht_door', lazy=True)  # Relatie naar DigitalGoods

    def __repr__(self):
        return f'<Gekocht {self.gekochtid} door {self.userid} - {self.goodid}>'


class Favoriet(db.Model):
    __tablename__ = 'favorieten'

    # Primaire sleutel
    favorietid = db.Column(db.String, primary_key=True) 

    # Foreign keys
    userid = db.Column(db.String, db.ForeignKey('users.userid'), nullable=False)  # Verwijst naar Users.userid
    goodid = db.Column(db.String, db.ForeignKey('digitalgoods.goodid'), nullable=False)  # Verwijst naar DigitalGoods.goodid

    # Metadata
    createdat = db.Column(db.DateTime, default=datetime.datetime.utcnow)  # Datum van favoriet maken

    # Relaties
    user = db.relationship('Users', backref='favoriete_reizen', lazy=True)  # Relatie naar Users
    good = db.relationship('DigitalGoods', backref='favoriet_door', lazy=True)  # Relatie naar DigitalGoods

    def __repr__(self):
        return f'<Favoriet {self.favorietid} door {self.userid} - {self.goodid}>'