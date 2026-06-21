from . import db
from flask_login import UserMixin
from sqlalchemy import Sequence
from datetime import date


class User(UserMixin, db.Model):

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(50), nullable = False, unique = False)
    last_name = db.Column(db.String(50), nullable = True, unique = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    role = db.Column(db.String(20), unique = False, nullable = False, default = 'trekker')
    is_active = db.Column(db.Boolean, unique = False, nullable = False, default = True)
    is_approved = db.Column(db.Boolean, unique = False, nullable = False, default = True)
    is_blocked = db.Column(db.Boolean, unique = False, nullable = False, default = False)
    password = db.Column(db.String(120), nullable = False, unique = False)


class Trekker(db.Model):

    __tablename__ = 'trekkers'
    trekker_id = db.Column(
        db.String(20),
        Sequence('trekker-', start = 101, increment=1),
        primary_key = True
    )
    first_name = db.Column(db.String(50), nullable = False, unique = False)
    last_name = db.Column(db.String(50), nullable = True, unique = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    contact = db.Column(db.Integer, unique = True, nullable = False)
    bio = db.Column(db.Text(1000), nullable = True, unique = False)
    dob = db.Column(db.Date, nullable = True, unique = False)
    user_since = db.Column(db.Date, nullable = False, default = date.today())
    booking_id = db.relationship('Booking', back_populates='trekker_id')


class Staff(db.Model):
    __tablename__ = 'staffs'
    staff_id = db.Column(
        db.String(20),
        Sequence('staff-', start = 101, increment=1),
        primary_key = True
    )
    first_name = db.Column(db.String(50), nullable = False, unique = False)
    last_name = db.Column(db.String(50), nullable = True, unique = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    contact = db.Column(db.Integer, unique = True, nullable = False)
    bio = db.Column(db.Text(1000), nullable = True, unique = False)
    dob = db.Column(db.Date, nullable = True, unique = False)
    staff_since = db.Column(db.Date, nullable = False, default = date.today())
    assigned_trek_id = db.Column(db.String(20), nullable = True, unique = False)
    trek_id = db.relationship('Trek', back_populates='staff_id')


class Trek(db.Model):
    __tablename__ = 'treks'
    trek_id = db.Column(
        db.String(20),
        Sequence('trek-', start=101, increment=1),
        primary_key = True
    )
    trek_name = db.Column(db.String(50), nullable = False, unique = False)
    assigned_staff_id = db.Column(db.String(20),db.ForeignKey('staffs.staff_id'), nullable = True, unique = True)
    location = db.Column(db.String(100))
    difficulty = db.Column(db.String(20), nullable = False, unique = False, default = 'moderate')
    duration = db.Column(db.Integer, nullable = False, unique = False, default = 0)
    trek_status = db.Column(db.String(20), nullable = False, unique = False, default = 'upcoming')
    no_of_slots = db.Column(db.Integer, nullable = False, unique = True)
    no_of_bookings = db.Column(db.Integer, nullable = True, unique = False, default = 0)
    start_date = db.Column(db.Date, nullable = False, unique = False)
    end_date = db.Column(db.Date, nullable = False, unique = False)
    price = db.Column(db.Integer, nullable  = False, unique = False)
    description = db.Column(db.String(1000), nullable = False, unique = False)
    staff_id = db.relationship('Staff', back_populates='trek_id')

class Booking(db.Model):
    __tablename__ = 'bookings'
    booking_id = db.Column(
        db.String(20),
        Sequence('booking-', start=101, increment=1),
        primary_key = True
    )
    trek_id = db.Column(db.String(20), db.ForeignKey('treks.trek_id'), nullable = False, unique = False)
    user_id = db.Column(db.String(20), db.ForeignKey('trekkers.trekker_id'), nullable = False, unique = False)
    trekker_id = db.relationship('Trekker', back_populates='booking_id')

# class UserHistory(db.Model):
#     __tablename__ = "users_history"
#     id = db.Column(db.Integer, primary_key = True)
    # first_name = db.Column(db.String(50), nullable = False, unique = False)
    # last_name = db.Column(db.String(50), nullable = True, unique = False)
    # email = db.Column(db.String(120), unique = True, nullable = False)
    # username = db.Column(db.String(120), unique = True, nullable = False)
    # role = db.Column(db.String(20), unique = False, nullable = False, default = 'not_defined')
    # account_status = db.Column(db.String(20), unique = False, nullable = False, default = 'active')
    # user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable  = False, unique = True)


# class TrekHistory(db.Model):
#     __tablename__ = 'trek_history'
#     id = db.Column(db.Integer, primary_key = True)
#     trek_id = db.Column(db.Integer, nullable = False, unique = True)
#     user_id = db.Column(db.Integer, nullable = False, unique = False)
#     staff_id = db.Column(db.Integer, nullable = False, unique = False)
#     trek_status = db.Column(db.String(20), nullable = False, unique = False, default = 'completed')
#     register_user = db.Column(db.Integer, nullable = False, unique = False, default = 0)
#     costs = db.Column(db.Integer, nullable = False, unique = False, default = 0)
#     earning = db.Column(db.Integer, nullable = False, unique = False, default = 0)
#     difficulty = db.Column(db.String(20), nullable = False, unique = False, default = 'medium')
#     duration = db.Column(db.Integer, nullable = False, unique = False, default = 0)
