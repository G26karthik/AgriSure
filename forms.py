from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, DateField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, Regexp, Optional
# Import the global users dictionary directly
from models import users

# Define choices for profession and district
PROFESSION_CHOICES = [('Farmer', 'Farmer'), ('Agent', 'Agent')]
DISTRICT_CHOICES = [ # Example districts - replace with actual list
    ('', '-- Select District --'),
    ('District A', 'District A'),
    ('District B', 'District B'),
    ('District C', 'District C'),
    # Add more districts as needed
]

class RegistrationForm(FlaskForm):
    profession = SelectField('Register as', choices=PROFESSION_CHOICES, validators=[DataRequired()])
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    phone_number = StringField('Phone Number', validators=[
        DataRequired(),
        Regexp(r'^\+?1?\d{9,15}$', message="Please enter a valid phone number.")
    ])
    address = StringField('Address', validators=[Optional(), Length(max=200)]) # Optional address
    dob = DateField('Date of Birth', format='%Y-%m-%d', validators=[Optional()]) # Optional DOB
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match.')
    ])
    district = SelectField('District (Agents only)', choices=DISTRICT_CHOICES, validators=[Optional()]) # Optional district
    submit = SubmitField('Register')

    # Custom validator to check if phone number already exists in the in-memory dictionary
    def validate_phone_number(self, phone_number):
        # Check the global users dictionary
        if phone_number.data in users:
            raise ValidationError('That phone number is already registered. Please choose a different one or login.')

    # Custom validator to make district required only if profession is Agent
    def validate_district(self, district):
        if self.profession.data == 'Agent' and not district.data:
            raise ValidationError('District is required for Agents.')


class LoginForm(FlaskForm):
    profession = SelectField('Login as', choices=PROFESSION_CHOICES, validators=[DataRequired()])
    phone_number = StringField('Phone Number', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')
    clear = SubmitField('Clear', render_kw={'formnovalidate': True, 'onclick': 'this.form.reset(); return false;'})
