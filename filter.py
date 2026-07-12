from models.model import Trek, User, Booking
from sqlalchemy import desc, asc


# ===== Trek Filter ======
def trek_filter(query, difficulty=None, status=None):
    if difficulty:
        query = query.filter(Trek.difficulty == difficulty)
    if status:
        query = query.filter(Trek.trek_status == status)
    return query

# ===== Trek Sort ======
def trek_sort(query, sort='created_at', orderby='desc'):

    if sort == 'created_at':
        if orderby == 'desc':
            query = query.order_by(Trek.created_at.desc(), Trek.id.desc())
            return query
        else:
            query = query.order_by(Trek.created_at.asc(), Trek.id.desc())
            return query
        
    if sort == 'duration':
        if orderby == 'desc':
            query = query.order_by(Trek.duration.desc(), Trek.id.desc())
            return query
        else:
            query = query.order_by(Trek.duration.asc(), Trek.id.desc())
            return query
        
    if sort == 'price':
        if orderby == 'desc':
            query = query.order_by(Trek.price.desc(), Trek.id.desc())
            return query
        else:
            query = query.order_by(Trek.price.asc(), Trek.id.desc())
            return query
        
    if sort == 'trek_code':
        if orderby == 'desc':
            query = query.order_by(Trek.trek_code.desc(), Trek.id.desc())
            return query
        else:
            query = query.order_by(Trek.trek_code.asc(), Trek.id.desc())
            return query
        
    if sort == 'trek_name':
        if orderby == 'desc':
            query = query.order_by(Trek.trek_name.desc(), Trek.id.desc())
            return query
        else:
            query = query.order_by(Trek.trek_name.asc(), Trek.id.desc())
            return query



# ===== Booking Filter ======
def booking_filter(query, status=None):
    if status:
        query = query.filter(Booking.status == status)
    return query

# ===== Booking Sort ======
def booking_sort(query, sort='booking_date', orderby='desc'):

    if sort == 'booking_date':
        if orderby == 'desc':
            query = query.order_by(Booking.booking_date.desc(), Booking.id.desc())
            return query
        else:
            query = query.order_by(Booking.booking_date.asc(), Booking.id.desc())
            return query
        
    if sort == 'trekker_id':
        if orderby == 'desc':
            query = query.order_by(Booking.trekker_id.desc(), Booking.id.desc())
            return query
        else:
            query = query.order_by(Booking.trekker_id.asc(), Booking.id.desc())
            return query
        
    if sort == 'price':
        if orderby == 'desc':
            query = query.order_by(Booking.id.desc(), Booking.id.desc())
            return query
        else:
            query = query.order_by(Booking.id.asc(), Booking.id.desc())
            return query


def user_filter(query, is_approved=None, is_active=None, is_blocked=None):
    if is_active == 'yes':
        query = query.filter(User.is_active == True)
    elif is_active == 'no':
        query = query.filter(User.is_active == False)
    
    if is_blocked == 'yes':
        query = query.filter(User.is_blocked == True)
    elif is_blocked == 'no':
        query = query.filter(User.is_blocked == False)
    
    if is_approved == 'yes':
        query = query.filter(User.is_approved== True)
    elif is_approved == 'no':
        query = query.filter(User.is_approved == False)
    
    return query

def user_sort(query, sort='created_at', orderby='asc'):
    if sort == 'created_at':
        if orderby == 'desc':
            query = query.order_by(User.created_at.desc(), User.id.desc())
            return query
        else:
            query = query.order_by(User.created_at.asc(), User.id.desc())
            return query
    if sort == 'email':
        if orderby == 'desc':
            query = query.order_by(User.email.desc(), User.id.desc())
            return query
        else:
            query = query.order_by(User.email.asc(), User.id.desc())
            return query
    if sort == 'first_name':
        if orderby == 'desc':
            query = query.order_by(User.first_name.desc(), User.last_name.desc(), User.id.desc())
            return query
        else:
            query = query.order_by(User.first_name.asc(),User.last_name.asc(), User.id.desc())
            return query
    return query
        

