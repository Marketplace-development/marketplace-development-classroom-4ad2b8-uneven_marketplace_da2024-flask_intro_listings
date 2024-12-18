from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField, DecimalField, SelectField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, InputRequired, Optional
from .models import db

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
        'Enter the price for your recipe (in USD):',
        validators=[DataRequired(), NumberRange(min=0)],
        places=2
    )

class RecipeRegionForm(FlaskForm):
    region = SelectField(
        'Region',
        choices=[
            ('belgium', 'Belgium'),
            ('italy', 'Italy'),
            ('china', 'China'),
            ('france', 'France'),
            ('japan', 'Japan'),
            ('thailand', 'Thailand'),
            ('mexico', 'Mexico'),
            ('india', 'India'),
            ('spain', 'Spain'),
            ('greece', 'Greece'),
            ('morocco', 'Morocco'),
            ('turkey', 'Turkey'),
            ('lebanon', 'Lebanon'),
            ('america', 'America'),
            ('caribbean', 'Caribbean'),
            ('south korea', 'South Korea'),
            ('russia', 'Russia'),
            ('germany', 'Germany'),
            ('vietnam', 'Vietnam'),
            ('portugal', 'Portugal'),
            ('brasil', 'Brasil'),
            ('south africa', 'South Africa'),
            ('peru', 'Peru'),
            ('australia', 'Australia'),
            ('philippines', 'Philippines'),
            ('britain', 'Britain'),
            ('sweden', 'Sweden'),
            ('indonesia', 'Indonesia'),
            ('arab world', 'Arab world'),
            ('pakistan', 'Pakistan'),
            ('other', 'Other')
        ],
        validators=[InputRequired()]
    )

class RecipeDurationForm(FlaskForm):
    duration = IntegerField(
        'Duration (in minutes)',
        validators=[
            InputRequired(),
            NumberRange(min=0, message="Duration must be 0 or greater.")
        ]
    )

class RatingForm(FlaskForm):
    rating = IntegerField('Rating (1-5)', validators=[DataRequired(), NumberRange(min=1, max=5)])
    review = TextAreaField('Review (optional)', validators=[Optional()])
    submit = SubmitField('Submit Review')