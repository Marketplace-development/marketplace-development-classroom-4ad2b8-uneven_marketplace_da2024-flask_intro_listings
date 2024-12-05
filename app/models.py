from flask_sqlalchemy import SQLAlchemy
from . import db 

db = SQLAlchemy()

# User Model (represents the 'customers' table in Supabase)
class User(db.Model):
    __tablename__ = 'customers'  # Matches 'customers' in Supabase
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    date_of_birth = db.Column(db.Date, nullable=True)
    country = db.Column(db.String(50), nullable=True)
    city = db.Column(db.String(50), nullable=True)
    postcode = db.Column(db.String(20), nullable=True)
    address = db.Column(db.String(200), nullable=True)
    language = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        return f"<User {self.username}>"

# Category Model (represents the 'categories' table in Supabase)
class Category(db.Model):
    __tablename__ = 'categories'  # Matches 'categories' in Supabase
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<Category {self.name}>"

# Recipe Model (represents the 'recipes' table in Supabase)
class Recipe(db.Model):
    __tablename__ = 'recipes'  # Matches 'recipes' in Supabase
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)  # Foreign key to 'customers'
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)  # Foreign key to 'categories'
    price = db.Column(db.Numeric, nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    user = db.relationship('User', backref='recipes')
    category = db.relationship('Category', backref='recipes')

    def __repr__(self):
        return f"<Recipe {self.title}>"

# Rating Model (represents the 'ratings' table in Supabase)
class Rating(db.Model):
    __tablename__ = 'ratings'  # Matches 'ratings' in Supabase
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), nullable=False)  # Foreign key to 'recipes'
    user_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)  # Foreign key to 'customers'
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    recipe = db.relationship('Recipe', backref='ratings')
    user = db.relationship('User', backref='ratings')

    def __repr__(self):
        return f"<Rating {self.rating} for Recipe {self.recipe_id}>"

# Example: Product Model (represents 'products' table in Supabase)
class Product(db.Model):
    __tablename__ = 'products'  # Matches 'products' in Supabase
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Numeric, nullable=False)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'), nullable=False)  # Foreign key to 'suppliers'

    supplier = db.relationship('Supplier', backref='products')

    def __repr__(self):
        return f"<Product {self.name}>"

# Supplier Model (represents the 'suppliers' table in Supabase)
class Supplier(db.Model):
    __tablename__ = 'suppliers'  # Matches 'suppliers' in Supabase
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<Supplier {self.name}>"