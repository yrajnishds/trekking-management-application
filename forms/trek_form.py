from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField, RadioField
from wtforms.validators import DataRequired, Email, Length, EqualTo, InputRequired

class TrekAddForm(FlaskForm):
    pass
class TrekBookForm(FlaskForm):
    pass

class TrekUpdateForm(FlaskForm):
    pass
