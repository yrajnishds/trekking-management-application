from sqlalchemy import or_

from models.model import User, TrekkerProfile, StaffProfile
from models.model import Trek, Booking


def admin_search_users(search):
    query = User.query
    if search:
        query = query.filter(
            or_(
                User.first_name.ilike(f"%{search}%"),
                User.last_name.ilike(f"%{search}%"),
                User.email.ilike(f"%{search}%"),
                User.role.ilike(f"%{search}%")
            )
        )
    return query

def admin_search_treks(search):
    query = Trek.query
    if search:
        query = query.filter(
            or_(
                Trek.trek_code.ilike(f"%{search}%"),
                Trek.trek_name.ilike(f"%{search}%"),
                Trek.location.ilike(f"%{search}%"),
                Trek.difficulty.ilike(f"%{search}%"),
                Trek.trek_status.ilike(f"%{search}%")
            )
        )
    return query

def admin_search_bookings(search):
    query = (
        Booking.query
        .join(Trek)
        .join(TrekkerProfile)
        .join(User)
    )
    if search:
        query = query.filter(
            or_(
                Trek.trek_name.ilike(f"%{search}%"),
                Trek.trek_code.ilike(f"%{search}%"),
                User.first_name.ilike(f"%{search}%"),
                User.last_name.ilike(f"%{search}%"),
                Booking.status.ilike(f"%{search}%")
            )
        )
    return query

def admin_search(search):
    return {
        "users": admin_search_users(search).all(),
        "treks": admin_search_treks(search).all(),
        "bookings": admin_search_bookings(search).all()
    }


def search_my_bookings(trekker_id, search):
    query = (
        Booking.query
        .join(Trek)
        .filter(
            Booking.trekker_id == trekker_id
        )
    )
    if search:
        query = query.filter(
            or_(
                Trek.trek_name.ilike(f"%{search}%"),
                Trek.location.ilike(f"%{search}%"),
                Booking.status.ilike(f"%{search}%")
            )
        )
    return query

def search_available_treks(trekker_id, search):
    query = Trek.query.filter(
        or_(
            Trek.trek_status == "upcoming",
            Trek.trek_status == "open",
        )
        
    )
    if search:
        query = query.filter(
            or_(
                Trek.trek_code.ilike(f"%{search}%"),
                Trek.trek_name.ilike(f"%{search}%"),
                Trek.location.ilike(f"%{search}%"),
                Trek.trek_status.ilike(f"%{search}%"),
                Trek.difficulty.ilike(f"%{search}%")
            )
        )
    return query

def trekker_search(trekker_id, search):
    return {
        'bookings': search_my_bookings(trekker_id, search).all(),
        'available_treks': search_available_treks(trekker_id, search).all()
    }


def search_staff_treks(staff_id, search):
    query = Trek.query.filter(
        Trek.staff_id == staff_id
    )
    if search:
        query = query.filter(
            or_(
                Trek.trek_name.ilike(f"%{search}%"),
                Trek.location.ilike(f"%{search}%"),
                Trek.trek_status.ilike(f"%{search}%")
            )
        )
    return query

def search_staff_bookings(staff_id, search):
    query = (
        Booking.query
        .join(Trek)
        .join(TrekkerProfile)
        .join(User)
        .filter(Trek.staff_id == staff_id)
    )
    if search:
        query = query.filter(
            or_(
                Trek.trek_name.ilike(f"%{search}%"),
                User.first_name.ilike(f"%{search}%"),
                User.last_name.ilike(f"%{search}%"),
                Booking.status.ilike(f"%{search}%")
            )
        )
    return query

def staff_search(staff_id, search):
    return {
        'treks': search_staff_treks(staff_id, search).all(),
        'bookings': search_staff_bookings(staff_id, search).all()
    }