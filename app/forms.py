from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, TextAreaField, SelectField, DateField, SubmitField, BooleanField, DecimalField
from wtforms.validators import DataRequired, Length, Regexp, NumberRange, ValidationError, Optional, Email
from flask_wtf.file import FileAllowed, FileField
from datetime import datetime

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(max=50)])
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=50)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    phone_number = StringField('Phone Number', validators=[Length(max=15)])
    street = StringField('Street', validators=[DataRequired()])
    street_number = StringField('Street Number', validators=[DataRequired()])
    postcode = StringField('Zip Code', validators=[DataRequired()])
    country = StringField('Country', validators=[DataRequired()])
    submit = SubmitField('Register')



class LoginForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=1, max=20)])
    remember = BooleanField('Remember Me')                                          #nog te arrangeren dat dat echt gebeurd
    submit = SubmitField('Login')


class ListingForm(FlaskForm):
    title = StringField(
        "title",
        validators=[
            DataRequired(message="Title is required."),
            Length(max=20, message="Title cannot exceed 20 characters."),
            Regexp(r'^[a-zA-Z0-9\s\-_#()]*$',
                   message="Title contains disallowed characters.")
        ]
    )
    picture = FileField(
        "picture",
        validators=[
            FileAllowed(['jpg', 'jpeg', 'png'], message="Only image files (jpg, jpeg, png) are allowed."),
        ]
    )
    base_price = StringField(
        "Base Price",
        validators=[
            DataRequired(message="Price is required."),
            Regexp(
                r'^\d{1,4}(\.\d{1,2})?$',
                message="Price must be a valid number with up to 4 whole digits and 2 decimal places."
            ),
            Length(max=7, message="Price cannot exceed 7 characters (e.g., 9999.99)."),
        ]
    )
    specie = StringField(
        "specie",
        validators=[
            DataRequired(message="Category is required."),
            Length(max=20, message="Category cannot exceed 20 characters."),
            Regexp(r'^[a-zA-Z\s\-]*$', message="Category contains disallowed characters."),

        ]
    )
    water = StringField(
        "water",
        validators=[
            DataRequired(message="Water is required."),
            Regexp(
                r'^\d{1,2}(\.\d{1,2})?$',
                message="Water must be a valid number with up to 2 whole digits and 2 decimal places."
            ),
            Length(max=5, message="Water cannot exceed 5 characters (e.g., 99.99l)."),
        ]
    )
    light = IntegerField(
        "light",
        validators=[
            DataRequired(message="Light requirement is required.")
        ]
    )
    nutrient = SelectField(
        'Nutrient',
        choices=[('None', 'None'), ('Fertilizer', 'Fertilizer'), ('Minerals', 'Minerals')],
        validators=[DataRequired(message="Nutrient selection is required.")]
    )
    pruning = TextAreaField(
        'Pruning Instructions',
        validators=[Length(max=100, message="Pruning instructions cannot exceed 100 characters.")]
    )
    sensitivity = SelectField(
        'Sensitivity',
        choices=[
            ('very_low', 'Very Low'),
            ('low', 'Low'),
            ('average', 'Average'),
            ('high', 'High'),
            ('very_high', 'Very High')
        ],
        validators=[DataRequired(message="Sensitivity selection is required.")]
    )
    start_date = DateField(
        'Start Date',
        format='%Y-%m-%d',
        validators=[DataRequired(message="Start date is required.")]
    )
    end_date = DateField(
        'End Date',
        format='%Y-%m-%d',
        validators=[DataRequired(message="End date is required.")]
    )

    street = StringField(
        'Street',
        validators=[DataRequired(message="Street is required."), Length(max=100)]
    )
    street_number = StringField(
        'Street Number',
        validators=[DataRequired(message="Street Number is required."), Length(max=10)]
    )
    city = StringField(
        'City',
        validators=[DataRequired(message="City is required."), Length(max=100)]
    )
    postcode = StringField(
        'Postcode',
        validators=[DataRequired(message="Postcode is required."), Length(max=10)]
    )
    country = StringField(
        'Country',
        validators=[DataRequired(message="Country is required."), Length(max=100)]
    )
    latitude = DecimalField(
        'Latitude',
        validators=[Optional()]
    )
    longitude = DecimalField(
        'Longitude',
        validators=[Optional()]
    )
    def validate_light(self, field):
        if field.data < 0:
            raise ValidationError("Light must be greater than or equal to 0.")

    def validate_start_date(self, field):
        """Validatie voor de startdatum"""
        if field.data and field.data <= datetime.today().date():
            raise ValidationError("Start date must be in the future.")

    def validate_end_date(self, field):
        """Validatie voor de einddatum"""
        if field.data and field.data <= datetime.today().date():
            raise ValidationError("End date must be in the future.")
        if self.start_date.data and field.data <= self.start_date.data:
            raise ValidationError("End date must be after the start date.")

    def validate_price_whole(self, field):
        if not field.data.isdigit():
            raise ValidationError("Price can only contain numbers.")
        if len(field.data) > 4:
            raise ValidationError("Price cannot be higher than $9999.99.")

    def validate_price_decimal(self, field):
        if not field.data.isdigit() or len(field.data) > 2:
            raise ValidationError("Price can contain maximum 2 decimals.")

    def validate_water_whole(self, field):
        if not field.data.isdigit():
            raise ValidationError("Water can only contain numbers.")
        if len(field.data) > 2:
            raise ValidationError("Water cannot be higher than 99.99l.")

    def validate_water_decimal(self, field):
        if not field.data.isdigit() or len(field.data) > 2:
            raise ValidationError("Water can contain maximum 2 decimals.")

    # Submit
    submit = SubmitField('Create Listing')

class ReviewForm(FlaskForm):
    rating = IntegerField('Rating (1-5)', validators=[DataRequired(), NumberRange(min=1, max=5)])
    feedback = TextAreaField('Feedback', validators=[DataRequired()])
    submit = SubmitField('Submit Review')
