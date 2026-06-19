from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField
from wtforms import EmailField, SubmitField, RadioField
from wtforms import DateField, TextAreaField
from wtforms.validators import DataRequired, Email, Length
from wtforms.validators import EqualTo, Optional

class TrekkerRegisterForm(FlaskForm):
    name = StringField(
        'Name',
        validators=[DataRequired(message='Enter your name.'),
                    Length(min=3, max=50, message='Name must be between 3 and 50 characters.')]
    )
    email = EmailField(
        'Email',
        validators=[DataRequired(message='Email Required'),
                    Email(message='Please enter a valid email address.')]
    )
    contact = IntegerField(
        'Contact No', validators=[DataRequired(message='Provide Contact Number'),
                                  Length(min=10, max=10, message='Contact Number Should be 10 digits Only')]
    )
    role = RadioField(
        'Role',
        validators=[DataRequired()],
        choices=[('trekker', 'Trekker')],
        default='trekker'
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired(message='Enter the Password'),
                    Length(min=3, message='Password Must Atleast 4 characters')]
    )
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[DataRequired(message='Enter the Confirm Password'),
                    EqualTo('password', message='Password and Confirm Password Must be same.')]
    )
    submit = SubmitField('Register')


class StaffRegisterForm(FlaskForm):
    name = StringField(
        'Name',
        validators=[DataRequired(message='Enter your name.'),
                    Length(min=3, max=50, message='Name must be between 3 and 50 characters.')]
    )
    email = EmailField(
        'Email',
        validators=[DataRequired(message='Email Required'),
                    Email(message='Please enter a valid email address.')]
    )
    contact = IntegerField(
        'Contact No', validators=[DataRequired(message='Provide Contact Number'),
                                  Length(min=10, max=10, message='Contact Number Should be 10 digits Only')]
    )
    role = RadioField(
        'Role',
        validators=[DataRequired()],
        choices=[('staff', 'Staff')],
        default='staff'
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired(message='Enter the Password'),
                    Length(min=3, message='Password Must Atleast 4 characters')]
    )
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[DataRequired(message='Enter the Confirm Password'),
                    EqualTo('password', message='Password and Confirm Password Must be same.')]
    )
    submit = SubmitField('Register')



class LoginForm(FlaskForm):
    email = EmailField(
        'Email',
        validators=[DataRequired(message='Email Required'),
                    Email(message='Please enter a valid email address.')]
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired(message='Enter the Password'),
                    Length(min=3, message='Password Must Atleast 4 characters')]
    )
    submit = SubmitField('Login')



class UsersAddForm(FlaskForm):
    name = StringField(
        'Name',
        validators=[DataRequired(message='Enter your name.'),
                    Length(min=3, max=50, message='Name must be between 3 and 50 characters.')]
    )
    email = EmailField(
        'Email',
        validators=[DataRequired(message='Email Required'),
                    Email(message='Please enter a valid email address.')]
    )
    contact = IntegerField(
        'Contact No', validators=[DataRequired(message='Provide Contact Number'),
                                  Length(min=10, max=10, message='Contact Number Should be 10 digits Only')]
    )
    role = RadioField(
        'Role',
        validators=[DataRequired()],
        choices=[('trekker', 'Trekker'),('staff', 'Staff')],
        default='staff'
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired(message='Enter the Password'),
                    Length(min=3, message='Password Must Atleast 4 characters')]
    )
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[DataRequired(message='Enter the Confirm Password'),
                    EqualTo('password', message='Password and Confirm Password Must be same.')]
    )
    submit = SubmitField('Add')



class ProfileUpdateForm(FlaskForm):
    name = StringField(
        'Name',
        validators=[Optional(),
                    Length(min=3, max=50, message='Name must be between 3 and 50 characters.')]
    )
    contact = IntegerField(
        'Contact No', validators=[Optional(),
                    Length(min=10, max=10, message='Contact Number Should be 10 digits Only')]
    )
    dob = DateField(
        'Date of Birth',
        validators=[Optional()]
    )
    bio = TextAreaField(
        'About Me',
        validators=[Optional(),
                    Length(min=0, max=1000, message='About me must be less than 1000 characters')]
    )
    password = PasswordField(
        'Password',
        validators=[Optional(),
                    Length(min=3, message='Password Must Atleast 4 characters'),
                    Length(min=3, message='Password Must Atleast 4 characters')]
    )
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[
                    EqualTo('password', message='Password and Confirm Password Must be same.')]
    )
    submit = SubmitField('Update')
    


