from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user, login_required
from models.model import User
from routes.decorators import role_required

staff_bp = Blueprint('staff', __name__, url_prefix='/staff')

@staff_bp.route('/')
@login_required
@role_required('staff')
def staff():
    return redirect(url_for('staff.dashboard'))


@staff_bp.route('/dashboard')
@login_required
@role_required('staff')
def dashboard():
    user_id = current_user.id
    user_data = User.query.filter_by(id = user_id).first()
    return render_template('staff/dashboard.html',
                           page = 'dashboard', first_name = user_data.first_name,
                           email = user_data.email,
                           role = user_data.role,
                           user_status = user_data.user_status)

@staff_bp.route('/profile')
@login_required
@role_required('staff')
def profile():
    user_id = current_user.id
    user_data = User.query.filter_by(id = user_id).first()


    return render_template('staff/profile.html',
                           page = 'profile', first_name = user_data.first_name,
                           email = user_data.email,
                           role = user_data.role,
                           user_status = user_data.user_status)

@staff_bp.route('/trek')
@login_required
@role_required('staff')
def assigned_trek():
    user_id = current_user.id
    user_data = User.query.filter_by(id = user_id).first()
    return render_template('staff/trek.html',
                           page = 'Treks', first_name = user_data.first_name,
                           email = user_data.email,
                           role = user_data.role,
                           user_status = user_data.user_status)

@staff_bp.route('/booking')
@login_required
@role_required('staff')
def booking():
    user_id = current_user.id
    user_data = User.query.filter_by(id = user_id).first()
    return render_template('staff/booking.html',
                           page = 'booking', first_name = user_data.first_name,
                           email = user_data.email,
                           role = user_data.role,
                           user_status = user_data.user_status)

@staff_bp.route('/history')
@login_required
@role_required('staff')
def history():
    user_id = current_user.id
    user_data = User.query.filter_by(id = user_id).first()

    return render_template('staff/history.html',
                           page = "history", first_name = user_data.first_name,
                           email = user_data.email,
                           role = user_data.role,
                           user_status = user_data.user_status)

