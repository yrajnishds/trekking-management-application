from flask import Blueprint,  render_template

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/')
@admin_bp.route('/dashboard')
def dashboard():
    return render_template('admin/dashboard.html', page = 'dashboard')

@admin_bp.route('/user')
def user():
    return render_template('admin/user.html', page = 'Users')

@admin_bp.route('/trek')
def trek():
    return render_template('admin/trek.html', page = 'Treks')

@admin_bp.route('/booking')
def booking():
    return render_template('admin/booking.html', page = 'booking')

@admin_bp.route('/history')
def history():
    return render_template('admin/history.html', page = 'history')

