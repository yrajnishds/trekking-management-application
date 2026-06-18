from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user, login_required
from models import db
from models.model import User
from routes.decorators import role_required



trekker_bp = Blueprint('trekker', __name__)


@trekker_bp.route('/dashboard')
@login_required
@role_required('trekker')
def dashboard():
    trekker_id = current_user.id
    trekker_data = User.query.filter_by(id = trekker_id).first()
    return render_template('trekker/dashboard.html',
                           page = 'dashboard', first_name = trekker_data.first_name,
                           email = trekker_data.email,
                           role = trekker_data.role)

@trekker_bp.route('/profile')
@login_required
@role_required('trekker')
def profile():
    trekker_id = current_user.id
    trekker_data = User.query.filter_by(id = trekker_id).first()


    return render_template('trekker/profile.html',
                           page = 'profile', first_name = trekker_data.first_name,
                           email = trekker_data.email,
                           role = trekker_data.role)

@trekker_bp.route('/trek')
@login_required
@role_required('trekker')
def trek():
    trekker_id = current_user.id
    trekker_data = User.query.filter_by(id = trekker_id).first()
    return render_template('trekker/trek.html',
                           page = 'Treks', first_name = trekker_data.first_name,
                           email = trekker_data.email,
                           role = trekker_data.role)

@trekker_bp.route('/booking')
@login_required
@role_required('trekker')
def booking():
    trekker_id = current_user.id
    trekker_data = User.query.filter_by(id = trekker_id).first()
    return render_template('trekker/booking.html',
                           page = 'booking', first_name = trekker_data.first_name,
                           email = trekker_data.email,
                           role = trekker_data.role)

@trekker_bp.route('/history')
@login_required
@role_required('trekker')
def history():
    trekker_id = current_user.id
    trekker_data = User.query.filter_by(id = trekker_id).first()

    return render_template('trekker/history.html',
                           page = "history", first_name = trekker_data.first_name,
                           email = trekker_data.email,
                           role = trekker_data.role)

