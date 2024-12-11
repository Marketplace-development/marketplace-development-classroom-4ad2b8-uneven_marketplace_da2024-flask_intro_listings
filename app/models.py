from app import db

class Customer(db.Model):
    __tablename__ = 'customers'
    customer_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    date_of_birth = db.Column(db.Date)
    address = db.Column(db.String)
    city = db.Column(db.String)
    country = db.Column(db.String)
    postcode = db.Column(db.String)
    language = db.Column(db.String)

class Recipe(db.Model):
    __tablename__ = 'recipes'
    recipe_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('customers.customer_id'), nullable=False)
    category_id = db.Column(db.String)
    price = db.Column(db.Numeric)
    ingredients = db.Column(db.String)
    image_url = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    steps = db.Column(db.Text, nullable=False)

class Rating(db.Model):
    __tablename__ = 'ratings'
    rating_id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.recipe_id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.customer_id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    review = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

class UserRecipe(db.Model):
    __tablename__ = 'user_recipes'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)

    # Relatie naar ingrediënten
    ingredients = db.relationship('Ingredient', backref='user_recipe', lazy=True)

class Ingredient(db.Model):
    __tablename__ = 'ingredients'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.String(50), nullable=False)
    user_recipe_id = db.Column(db.Integer, db.ForeignKey('user_recipes.id'), nullable=False)

class Favorite(db.Model):
    __tablename__ = 'favorites'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('customers.customer_id'), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.recipe_id'), nullable=False)

    user = db.relationship('Customer', backref='favorites', lazy=True)
    recipe = db.relationship('Recipe', backref='favorites', lazy=True)
