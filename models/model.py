from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date
class User(UserMixin, db.Model):

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(50), nullable = False, unique = False)
    last_name = db.Column(db.String(50), nullable = True, unique = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    username = db.Column(db.String(120), unique = True, nullable = True)
    role = db.Column(db.String(20), unique = False, nullable = False, default = 'not_defined')
    approval_status = db.Column(db.String(20), unique = False, nullable = False, default = 'not_approved')
    user_status = db.Column(db.String(20), unique = False, nullable = False, default = 'active')
    password_hash = db.Column(db.String(120), nullable = False, unique = False)
    bio = db.Column(db.Text(1000), nullable = True, unique = False)
    dob = db.Column(db.Date, nullable = True, unique = False)
    user_since = db.Column(db.Date, nullable = False, default = date.today())
    


    def set_password(self, password):
        """Hashes and stores the password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Checks if the plain password matches the stored hash."""
        return check_password_hash(self.password_hash, password)

# class UserProfile(db.Model):

#     __tablename__ = 'users_profile'
#     id = db.Column(db.Integer, primary_key = True)
#     # first_name = db.Column(db.String(50), nullable = False, unique = False)
#     # last_name = db.Column(db.String(50), nullable = True, unique = False)
#     # email = db.Column(db.String(120), unique = True, nullable = False)
#     # username = db.Column(db.String(120), unique = True, nullable = False)
#     # # is_active = db.Column(db.Boolean, default=True, nullable=False)
#     role = db.Column(db.String(20), unique = False, nullable = False, default = 'not_defined')
#     user_status = db.Column(db.String(20), unique = False, nullable = False, default = 'not_approved')
#     bio = db.Column(db.Text(1000), nullable = True, unique = False)
#     dob = db.Column(db.Date, nullable = True, unique = False)
#     user_since = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)




class Trek(db.Model):
    __tablename__ = 'treks'
    id = db.Column(db.Integer, primary_key = True)
    trek_name = db.Column(db.String(50), nullable = False, unique = False)
    trek_status = db.Column(db.String(20), nullable = False, unique = False, default = 'upcoming')
    difficulty = db.Column(db.String(20), nullable = False, unique = False, default = 'moderate')
    duration = db.Column(db.Integer, nullable = False, unique = False, default = 0)
    available_seats = db.Column(db.Integer, nullable = False, unique = True)
    price = db.Column(db.Integer, nullable  = False, unique = False)
    assigned_staff_id = db.Column(db.Integer, nullable = False, unique = False)
    description = db.Column(db.String(1000), nullable = False, unique = False)


class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key = True)
    trek_id = db.Column(db.Integer, nullable = False, unique = True)
    user_id = db.Column(db.Integer, nullable = False, unique = False)
    

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


class TrekHistory(db.Model):
    __tablename__ = 'trek_history'
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
