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