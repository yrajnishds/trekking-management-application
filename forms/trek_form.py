from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, TextAreaField
from wtforms import IntegerField, DateField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Length
from datetime import date, timedelta


class TrekAddForm(FlaskForm):
    trek_id = StringField(
        "Trek Id",
        validators=[DataRequired(message='Trek Id Required'),
                    Length(min=3, max=10, message='Id Must in Between 3 to 10 Characters')]
    )
    trek_name = StringField(
        'Trek Name',
        validators=[DataRequired(message='Trek name is required'),
                                 Length(min=3, max=50, message='Trek name Must In between 3 to 50 characters')]
    )
    location = StringField(
        'Trek Location',
        validators=[DataRequired(message='Trek location is required'),
                                 Length(min=3, max=100, message='Trek location Must In between 3 to 100 characters')]
    )
    difficulty = RadioField(
        'Difficulty',
        validators=[DataRequired(message='Difficulty level required')],
        choices=[('easy', 'Easy'), ('moderate', 'Moderate'), ('hard', 'Hard')],
        default='moderate'
    )
    duration = IntegerField(
        'Duration (In Days)',
        validators=[DataRequired(message='Duration must be not empty.'),
                    NumberRange(min=1, message='Please Provide a positive Number.')]
    )
    no_of_slots = IntegerField(
        'No of Slots',
        validators=[DataRequired(message='Please Provide number of available slots'),
                                 NumberRange(min=1, message='Please Provide a Positive Number greater than 1')]
    )
    trek_status = RadioField(
        'Trek Status',
        choices=[('pending', 'Pending'), ('approved', 'Approved'), ('open', 'Open')],
                 validators=[DataRequired(message='Please choose trek status.')]
    )
    start_date = DateField(
        'Start Date',
        validators=[DataRequired(message='Please Provide the start date')],
        default=date.today()
    )
    end_date = DateField(
        'End Date',
        validators=[DataRequired(message='Please Provide the start date')],
        default=date.today() + timedelta(days=7)
    )
    price = IntegerField(
        'Price',
        validators=[DataRequired(message='Please Provide the Cost'),
                    NumberRange(min=0, message='Price Must be greater than zero.')]
    )
    description = TextAreaField(
        'Description', default='Welcome to the Trek.'
    )
    submit = SubmitField('Create Trek')

class TrekBookForm(FlaskForm):
    pass

class TrekUpdateForm(FlaskForm):
    pass
