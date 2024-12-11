from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField
from wtforms.validators import DataRequired, Length

class TitleForm(FlaskForm):
    title = StringField('Recepttitel', validators=[DataRequired(), Length(max=100)])
    photo = FileField('Upload een afbeelding (optioneel)')

class DescriptionForm(FlaskForm):
    description = TextAreaField('Korte beschrijving', validators=[DataRequired()])

class IngredientsForm(FlaskForm):
    ingredients = TextAreaField('Ingrediënten', validators=[DataRequired()])

class StepsForm(FlaskForm):
    steps = TextAreaField('Bereidingsstappen', validators=[DataRequired()])
