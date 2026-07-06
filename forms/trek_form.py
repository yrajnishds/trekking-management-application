from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, TextAreaField
from wtforms import IntegerField, DateField, SubmitField
from wtforms import SelectField
from wtforms.validators import DataRequired, NumberRange, Length
from wtforms.validators import Optional
from datetime import date, timedelta


class TrekAddForm(FlaskForm):
    trek_code = StringField(
        'Trek Code',
        validators=[DataRequired(message='Trek Code is required'),
                                 Length(min=3, max=20, message='Trek COde Must In between 3 to 20 characters')]
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
        default=date.today() + timedelta(days=7)
    )
    end_date = DateField(
        'End Date',
        validators=[DataRequired(message='Please Provide the start date')],
        default=date.today() + timedelta(days=14)
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
    trek_id = SelectField(
        'Select Trek',
        validators=[DataRequired(message='Select a Trek')],
        choices=[]
    )
    trekker_id = SelectField(
        'Select trekker',
        choices=[]
    )
    date = DateField(
        'Date', default=date.today(),
        validators=[DataRequired(message='Select the Booking date.')]
    )



class TrekUpdateForm(FlaskForm):
    trek_code = SelectField(
        'Trek Code',
        validators=[DataRequired(message='Trek Code is required')],
        choices=[]
    )
    trek_name = SelectField(
        'Trek Name',
        validators=[DataRequired(message='Trek name is required')],
        choices=[]
        )
    location = StringField(
        'Update Location',
        validators=[Optional(),
                    Length(min=3, max=100, message='Trek location Must In between 3 to 100 characters')]
    )
    difficulty = RadioField(
        'Update Difficulty',
        validators=[Optional()],
        choices=[('easy', 'Easy'), ('moderate', 'Moderate'), ('hard', 'Hard')]
    )
    duration = IntegerField(
        'Update Duration (In Days)',
        validators=[Optional(),
                    NumberRange(min=1, message='Please Provide a positive Number.')]
    )
    no_of_slots = IntegerField(
        'No of Slots',
        validators=[Optional(),
                    NumberRange(min=1, message='Please Provide a Positive Number greater than 1')]
    )

    start_date = DateField(
        'Start Date',
        validators=[Optional()]
    )
    end_date = DateField(
        'End Date',
        validators=[Optional()]
    )
    price = IntegerField(
        'Update Price',
        validators=[Optional(),
                    NumberRange(min=0, message='Price Must be greater than zero.')]
    )
    description = TextAreaField(
        'Description'
    )
    submit = SubmitField('Update Details')


class AssignStaffForm(FlaskForm):
    assigned_staff = SelectField(
        'Select Staff',
        validators=[DataRequired()], choices=[]
    )


class TrekActionForm(FlaskForm):
    trek_action = SelectField(
        'Select Status',
        validators=[DataRequired()],
        choices=[]
    )