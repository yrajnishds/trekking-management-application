from datetime import date

from flask_login import UserMixin

from . import db



# User

class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50))

    email = db.Column(db.String(120), unique=True, nullable=False)

    password = db.Column(db.String(255), nullable=False)

    role = db.Column(
        db.String(20),
        nullable=False,
        default="trekker"
    )

    is_active = db.Column(
        db.Boolean,
        nullable=False,
        default=True
    )

    is_approved = db.Column(
        db.Boolean,
        nullable=False,
        default=True
    )

    is_blocked = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )

    created_at = db.Column(
        db.Date,
        nullable=False,
        default=date.today
    )

    trekker_profile = db.relationship(
        "TrekkerProfile",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )

    staff_profile = db.relationship(
        "StaffProfile",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )

    admin_profile = db.relationship(
        "AdminProfile",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )



# Trekker Profile

class TrekkerProfile(db.Model):
    __tablename__ = "trekkers"

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        primary_key=True
    )

    contact = db.Column(db.String(15), unique=True)

    bio = db.Column(db.Text)

    dob = db.Column(db.Date)

    trekker_since = db.Column(
        db.Date,
        default=date.today,
        nullable=False
    )

    user = db.relationship(
        "User",
        back_populates="trekker_profile"
    )

    bookings = db.relationship(
        "Booking",
        back_populates="trekker",
        cascade="all, delete-orphan"
    )




# Staff Profile

class StaffProfile(db.Model):
    __tablename__ = "staffs"

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        primary_key=True
    )

    contact = db.Column(db.String(15), unique=True)

    bio = db.Column(db.Text)

    dob = db.Column(db.Date)

    staff_since = db.Column(
        db.Date,
        default=date.today,
        nullable=False
    )

    user = db.relationship(
        "User",
        back_populates="staff_profile"
    )

    treks = db.relationship(
        "Trek",
        back_populates="staff",
        cascade="all"
    )



# Admin Profile

class AdminProfile(db.Model):
    __tablename__ = "admin"

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        primary_key=True
    )

    contact = db.Column(db.String(15), unique=True)

    bio = db.Column(db.Text)

    dob = db.Column(db.Date)

    admin_since = db.Column(
        db.Date,
        default=date.today,
        nullable=False
    )

    user = db.relationship(
        "User",
        back_populates="admin_profile"
    )




# Trek

class Trek(db.Model):
    __tablename__ = "treks"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    trek_code = db.Column(
        db.String(20),
        unique=True,
        nullable=False
    )

    trek_name = db.Column(
        db.String(100),
        nullable=False
    )

    location = db.Column(
        db.String(100),
        nullable=False
    )

    difficulty = db.Column(
        db.String(20),
        nullable=False,
        default="Moderate"
    )

    duration = db.Column(
        db.Integer,
        nullable=False
    )

    start_date = db.Column(
        db.Date,
        nullable=False
    )

    end_date = db.Column(
        db.Date,
        nullable=False
    )

    trek_status = db.Column(
        db.String(20),
        nullable=False,
        default="Upcoming"
    )

    slots = db.Column(
        db.Integer,
        nullable=False
    )

    booked_slots = db.Column(
        db.Integer,
        nullable=False,
        default=0
    )

    price = db.Column(
        db.Integer,
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=False
    )

    staff_id = db.Column(
        db.Integer,
        db.ForeignKey("staffs.user_id")
    )

    staff = db.relationship(
        "StaffProfile",
        back_populates="treks"
    )

    bookings = db.relationship(
        "Booking",
        back_populates="trek",
        cascade="all, delete-orphan"
    )




# Booking

class Booking(db.Model):
    __tablename__ = "bookings"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    trek_id = db.Column(
        db.Integer,
        db.ForeignKey("treks.id"),
        nullable=False,
        unique=False

    )

    trekker_id = db.Column(
        db.Integer,
        db.ForeignKey("trekkers.user_id"),
        nullable=False,
        unique=False
    )

    booking_date = db.Column(
        db.Date,
        nullable=False,
        default=date.today
    )

    status = db.Column(
        db.String(20),
        nullable=False,
        default="pending"
    )

    amount_paid = db.Column(
        db.Integer,
        nullable=False,
        default=0
    )

    trek = db.relationship(
        "Trek",
        back_populates="bookings"
    )

    trekker = db.relationship(
        "TrekkerProfile",
        back_populates="bookings"
    )