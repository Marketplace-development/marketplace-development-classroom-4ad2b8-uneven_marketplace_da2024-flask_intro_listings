from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Recipe(db.Model):
    __tablename__ = 'Recipes'
    recipeID = db.Column(db.String, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    userID = db.Column(db.String, db.ForeignKey('Customers.customerID'))
    categoryID = db.Column(db.String, db.ForeignKey('Categories.categoryID'))
    price = db.Column(db.Numeric, nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    imageURL = db.Column(db.String)
    createdAt = db.Column(db.DateTime, default=db.func.current_timestamp())

class Rating(db.Model):
    __tablename__ = 'Ratings'
    ratingID = db.Column(db.String, primary_key=True)
    recipeID = db.Column(db.String, db.ForeignKey('Recipes.recipeID'))
    customerID = db.Column(db.String, db.ForeignKey('Customers.customerID'))
    rating = db.Column(db.Integer, nullable=False)
    review = db.Column(db.Text)
    createdAt = db.Column(db.DateTime, default=db.func.current_timestamp())


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    listings = db.relationship('Listing', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'
    
class Listing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    listing_name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Listing {self.listing_name}, ${self.price}>'