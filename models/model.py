from . import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(50), nullable = False, unique = False)
    last_name = db.Column(db.String(50), nullable = True, unique = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    username = db.Column(db.String(120), unique = True, nullable = False)
    role = db.Column(db.String(20), unique = False, nullable = False, default = 'not_approved')
    user_status = db.Column(db.String(20), unique = False, nullable = False, default = 'not_approved')
    password = db.Column(db.String(120), nullable = False, unique = False)


class Trek(db.Model):
    __tablename__ = 'treks'
    id = db.Column(db.Integer, primary_key = True)
    trek_name = db.Column(db.String(50), nullable = False, unique = False)
    trek_status = db.Column(db.String(20), nullable = False, unique = False, default = 'upcoming')
    difficulty = db.Column(db.String(20), nullable = False, unique = False, default = 'medium')
    duration = db.Column(db.Integer, nullable = False, unique = False)
    available_seats = db.Column(db.Integer, nullable = False, unique = True)
    price = db.Column(db.Integer, nullable  = False, unique = False)
    assigned_staff_id = db.Column(db.Integer, nullable = False, unique = False)
    description = db.Column(db.String(1000), nullable = False, unique = False)


class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key = True)
    trek_id = db.Column(db.Integer, nullable = False, unique = True)
    user_id = db.Column(db.Integer, nullable = False, unique = False)
    

class History(db.Model):
    __tablename__ = 'history'
    id = db.Column(db.Integer, primary_key = True)
    trek_id = db.Column(db.Integer, nullable = False, unique = True)
    user_id = db.Column(db.Integer, nullable = False, unique = False)
    staff_id = db.Column(db.Integer, nullable = False, unique = False)
    trek_status = db.Column(db.String(20), nullable = False, unique = False, default = 'completed')
    register_user = db.Column(db.Integer, nullable = False, unique = False, default = 0)
    costs = db.Column(db.Integer, nullable = False, unique = False, default = 0)
    earning = db.Column(db.Integer, nullable = False, unique = False, default = 0)
    difficulty = db.Column(db.String(20), nullable = False, unique = False, default = 'medium')
    duration = db.Column(db.Integer, nullable = False, unique = False, default = 0)
