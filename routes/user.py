from flask import Blueprint, render_template

user_bp = Blueprint('user', __name__, url_prefix='/user')

@user_bp.route('/')
@user_bp.route('/dashboard')
def dashboard():
    return render_template('user/dashboard.html', page = 'dashboard')

@user_bp.route('/profile')
def user():
    return render_template('user/profile.html', page = 'profile')

@user_bp.route('/trek')
def trek():
    return render_template('user/trek.html', page = 'Treks')

@user_bp.route('/booking')
def booking():
    return render_template('user/booking.html', page = 'booking')

@user_bp.route('/history')
def history():
    return render_template('user/history.html', page = "history")

