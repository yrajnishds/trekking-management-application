from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user, login_required
from models import db
from models.model import User
from routes.decorators import role_required



user_bp = Blueprint('user', __name__)


@user_bp.route('/dashboard')
@login_required
@role_required('user')
def dashboard():
    user_id = current_user.id
    user_data = User.query.filter_by(id = user_id).first()
    return render_template('user/dashboard.html',
                           page = 'dashboard', first_name = user_data.first_name,
                           email = user_data.email,
                           role = user_data.role,
                           user_status = user_data.user_status)

@user_bp.route('/profile')
@login_required
@role_required('user')
def profile():
    user_id = current_user.id
    user_data = User.query.filter_by(id = user_id).first()


    return render_template('user/profile.html',
                           page = 'profile', first_name = user_data.first_name,
                           email = user_data.email,
                           role = user_data.role,
                           user_status = user_data.user_status)

@user_bp.route('/trek')
@login_required
@role_required('user')
def trek():
    user_id = current_user.id
    user_data = User.query.filter_by(id = user_id).first()
    return render_template('user/trek.html',
                           page = 'Treks', first_name = user_data.first_name,
                           email = user_data.email,
                           role = user_data.role,
                           user_status = user_data.user_status)

@user_bp.route('/booking')
@login_required
@role_required('user')
def booking():
    user_id = current_user.id
    user_data = User.query.filter_by(id = user_id).first()
    return render_template('user/booking.html',
                           page = 'booking', first_name = user_data.first_name,
                           email = user_data.email,
                           role = user_data.role,
                           user_status = user_data.user_status)

@user_bp.route('/history')
@login_required
@role_required('user')
def history():
    user_id = current_user.id
    user_data = User.query.filter_by(id = user_id).first()

    return render_template('user/history.html',
                           page = "history", first_name = user_data.first_name,
                           email = user_data.email,
                           role = user_data.role,
                           user_status = user_data.user_status)

