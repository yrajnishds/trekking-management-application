from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField, RadioField
from wtforms import IntegerField
from wtforms.validators import DataRequired, Email, Length, EqualTo, InputRequired

class UserRegisterForm(FlaskForm):
    name = StringField('Name',
                       validators=[DataRequired(message='Please enter your name.'),
                                   Length(min=3, max=50, message='Name must be between 3 and 50 characters.')])
    email = EmailField('Email Address',
                       validators=[DataRequired(message='Please enter your email address.'),
                                   Email(message='Please enter a valid email address.')])
    role = RadioField('Role',
                      choices=[('user', 'User')], default='user')
    password = PasswordField('Password',
                             validators=[DataRequired(message='Please enter a password.'),
                                         Length(min=4, max=200, message='Password must be at least 4 characters long.')])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(message='Please confirm your password.'),
                                                 EqualTo('password', message='Passwords must match.')])
    submit = SubmitField('Register')

class StaffRegisterForm(FlaskForm):
    name = StringField('Name',
                            validators=[DataRequired(message='Please enter your name.'),
                                Length(min=3, max=50, message='Name must be between 3 and 50 characters.')])
    email = EmailField('Email Address',
                            validators=[DataRequired(message='Please enter your email address.'),
                                Email(message='Please enter a valid email address.')])
    role = RadioField('Role',
                            choices=[('staff', 'Staff')], default='staff')
    password = PasswordField('Password',
                            validators=[DataRequired(message='Please enter a password.'),
                                Length(min=4, max=200, message='Password must be at least 4 characters long.')])
    confirm_password = PasswordField('Confirm Password',
                            validators=[DataRequired(message='Please confirm your password.'),
                                EqualTo('password', message='Passwords must match.')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = EmailField('Email Address',
                            validators=[DataRequired(message='Please enter your email address.'),
                                Email(message='Please enter a valid email address.')])
    password = PasswordField('Password',
                                validators=[DataRequired(message='Please enter your password.')])
    submit = SubmitField('Login')

class AddUsersForm(FlaskForm):
    name = StringField('Name',
                            validators=[DataRequired(message='Please enter your name.'),
                                Length(min=3, max=50, message='Name must be between 3 and 50 characters.')])
    email = EmailField('Email Address',
                            validators=[DataRequired(message='Please enter your email address.'),
                                Email(message='Please enter a valid email address.')])
    role = RadioField('Role',
                            choices=[('user', 'User'), ('staff', 'Staff')],
                                validators=[InputRequired(message = 'Please Select a field.')])
    password = PasswordField('Password',
                                validators=[DataRequired(message='Please enter a password.'),
                                    Length(min=4, max=200, message='Password must be at least 4 characters long.')])
    confirm_password = PasswordField('Confirm Password',
                                        validators=[DataRequired(message='Please confirm your password.'),
                                            EqualTo('password', message='Passwords must match.')])
    submit = SubmitField('Add')

class TrekAddForm(FlaskForm):
    pass
class TrekBookForm(FlaskForm):
    pass

class TrekUpdateForm(FlaskForm):
    pass

class ProfileUpdateForm(FlaskForm):
    pass