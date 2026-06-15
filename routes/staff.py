from flask import Blueprint, render_template

staff_bp = Blueprint('staff', __name__, url_prefix='/staff')

@staff_bp.route('/')
@staff_bp.route('/dashboard')
def dashboard():
    return render_template('staff/dashboard.html', page = 'dashboard')

@staff_bp.route('/profile')
def staff():
    return render_template('staff/profile.html', page = 'profile')

@staff_bp.route('/trek')
def trek():
    return render_template('staff/trek.html', page = 'Treks')

@staff_bp.route('/booking')
def booking():
    return render_template('staff/booking.html', page = 'booking')

@staff_bp.route('/history')
def history():
    return render_template('staff/history.html', page = "history")

