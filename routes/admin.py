from flask import Blueprint,  render_template, redirect, url_for
from flask_login import current_user, login_required
from models.model import User
from routes.decorators import role_required

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/')
@login_required
@role_required('admin')
def admin():
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/dashboard')
@login_required
@role_required('admin')
def dashboard():
    user_id = current_user.id
    user_data = User.query.filter_by(id = user_id).first()
    return render_template('admin/dashboard.html',
                           page = f'dashboard', first_name = user_data.first_name,
                           email = user_data.email,
                           role = user_data.role)


@admin_bp.route('/user')
@login_required
@role_required('admin')
def user():
    user_id = current_user.id
    user_data = User.query.filter_by(id = user_id).first()
    return render_template('admin/user.html',
                           page = 'Users', first_name = user_data.first_name,
                           email = user_data.email,
                           role = user_data.role)

@admin_bp.route('/staff')
@login_required
@role_required('admin')
def staff():
    user_id = current_user.id
    user_data = User.query.filter_by(id = user_id).first()
    return render_template('admin/staff.html',
                           page = 'Staffs', first_name = user_data.first_name,
                           email = user_data.email,
                           role = user_data.role)


@admin_bp.route('/trek')
@login_required
@role_required('admin')
def trek():
    user_id = current_user.id
    user_data = User.query.filter_by(id = user_id).first()
    return render_template('admin/trek.html', page = 'Treks', first_name = user_data.first_name,
                           email = user_data.email,
                           role = user_data.role)


@admin_bp.route('/booking')
@login_required
@role_required('admin')
def booking():
    user_id = current_user.id
    user_data = User.query.filter_by(id = user_id).first()
    return render_template('admin/booking.html',page = 'booking', first_name = user_data.first_name,
                           email = user_data.email,
                           role = user_data.role)

@admin_bp.route('/history')
@login_required
@role_required('admin')
def history():
    user_id = current_user.id
    user_data = User.query.filter_by(id = user_id).first()
    return render_template('admin/history.html',
                           page = 'history', first_name = user_data.first_name,
                           email = user_data.email,
                           role = user_data.role)


@admin_bp.route('/profile')
@login_required
@role_required('admin')
def profile():
    user_id = current_user.id
    user_data = User.query.filter_by(id = user_id).first()
    return render_template('admin/profile.html',page = 'Profile', first_name = user_data.first_name,
                           email = user_data.email,
                           role = user_data.role)


