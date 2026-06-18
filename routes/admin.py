from flask import Blueprint,  render_template, redirect, url_for
from flask import request, flash
from flask_login import current_user, login_required
from models.model import User
from routes.decorators import role_required
from models import db
from forms.form import AddUsersForm

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
    users = User.query.filter_by(role = 'user').all()
    form = AddUsersForm()
    return render_template('admin/user.html',
                           page = 'Users', first_name = user_data.first_name,
                           email = user_data.email,
                           role = user_data.role,
                           users = users, form = form,
                           type = 'user')

@admin_bp.route('/add-user', methods = ['GET', 'POST'])
@login_required
@role_required('admin')
def add_user():
    form = AddUsersForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user:
            flash(f'{user.role.caplitalize()} With this email already exits', 'error')
            return redirect(url_for('auth.register'))
        
        else:
            name = form.name.data.split()
            if len(name) != 1:
                first_name = name[0]
                last_name = " ".join(name[1:])
            else:
                first_name = name[0]
                last_name = None
            email = form.email.data
            password = form.password.data
            role = form.role.data
            if role == 'user':
                approval_status = 'approved'
            else:
                approval_status = 'pending'
            new_user = User(first_name = first_name,
                            last_name = last_name,
                            email = email,
                            role = role,
                            approval_status = approval_status)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            flash(f'New {role.capitalize()} Added', 'success')
            if role == 'staff':
                flash(f'Now You Can Update {role.capitalize()} Approval Status', 'info')
            return redirect(url_for('admin.user'))
    return redirect(url_for('admin.user'))


@admin_bp.route('/user/<int:id>', methods = ['GET', 'POST'])
@login_required
@role_required('admin')
def user_block(id):
    user_id = id
    if request.method == "POST":
        user = User.query.filter_by(id = user_id).first()
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for('admin.user'))

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


