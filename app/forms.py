from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField, DecimalField
from wtforms.validators import DataRequired, Length, NumberRange

class TitleForm(FlaskForm):
    title = StringField('Recipe Title', validators=[DataRequired(), Length(max=100)])
    photo = FileField('Upload an Image (optional)')

class DescriptionForm(FlaskForm):
    description = TextAreaField('Give a brief description of your recipe', validators=[DataRequired()])

class IngredientsForm(FlaskForm):
    ingredients = TextAreaField('List Ingredients here...', validators=[DataRequired()])

class StepsForm(FlaskForm):
    steps = TextAreaField('Give detailed steps to prepare the recipe', validators=[DataRequired()])

class PriceForm(FlaskForm):
    price = DecimalField(
        'Enter the price for your recipe (in EUR):',
        validators=[DataRequired(), NumberRange(min=0)],
        places=2
    )
