from flask import Blueprint,  render_template, redirect, url_for
from flask import flash, request
from flask_login import current_user, login_required
from models.model import User
from routes.decorators import role_required
from models import db
from forms.user_form import AddUsersForm

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
    admin_id = current_user.id
    admin_data = User.query.filter_by(id = admin_id).first()
    return render_template('admin/dashboard.html',
                           page = f'dashboard', first_name = admin_data.first_name,
                           email = admin_data.email,
                           role = admin_data.role)


@admin_bp.route('/trekker')
@login_required
@role_required('admin')
def trekker():
    trekkers = User.query.filter_by(role = 'trekker').all()
    form = AddUsersForm()
    total = User.query.filter_by(role = 'trekker').count()
    approved = User.query.filter_by(role = 'trekker', approval_status = 'approved').count()
    pending = total - approved
    active = User.query.filter_by(role = 'trekker', is_active = True).count()
    inactive = total - active
    blacklisted = User.query.filter_by(role = 'trekker', is_blocked = True).count()
    unblacklisted = total - blacklisted

    return render_template('admin/trekker.html',
                           page = 'trekkers',
                           users = trekkers, form = form,
                           role_type = 'trekker',
                           total = total,
                           approved = approved,
                           pending = pending,
                           active = active,
                           inactive = inactive,
                           blacklisted = blacklisted,
                           unblacklisted = unblacklisted)

@admin_bp.route('/staff')
@login_required
@role_required('admin')
def staff():
    staffs = User.query.filter_by(role = 'staff').all()
    form = AddUsersForm()
    return render_template('admin/staff.html',
                           page = 'Staffs',
                           users = staffs, form = form,
                           role_type = 'staff')

@admin_bp.route('/add/<string:role_type>', methods = ['GET', 'POST'])
@login_required
@role_required('admin')
def add_user(role_type):
    form = AddUsersForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user:
            flash(f'{user.role.caplitalize()} With this email already exits', 'error')
            return redirect(url_for('auth.register'))
        
        else:
            name = form.name.data.strip().split()
            if len(name) != 1:
                first_name = name[0].lower()
                last_name = " ".join(name[1:]).lower()
            else:
                first_name = name[0].lower()
                last_name = None
            email = form.email.data
            password = form.password.data
            role = form.role.data
            if role == 'trekker':
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
            return redirect(url_for(f'admin.{role_type}'))
    return redirect(url_for(f'admin.{role_type}'))


@admin_bp.route('/<string:role_type>/<int:id>/<string:action>', methods = ['GET', 'POST'])
@login_required
@role_required('admin')
def admin_action(role_type, id, action):
    if request.method == 'POST':
        user_data = User.query.get_or_404(id)
        if not user_data:
            flash('Invalid Id', 'error')
            return redirect(url_for(f'admin.{role_type}'))
        if action == 'approved':
            user_data.approval_status = action
            db.session.commit()
            flash(f'Now Approval for {user_data.first_name} changed to {action}', 'success')
            return redirect(url_for(f'admin.{role_type}'))
        elif action == 'pending':
            user_data.approval_status = action
            db.session.commit()
            flash(f'Now Approval for {user_data.first_name} changed to {action}', 'info')
            return redirect(url_for(f'admin.{role_type}'))
        elif action == 'activate':
            user_data.is_active = True
            db.session.commit()
            flash(f'{user_data.first_name} is now Activated', 'success')
            return redirect(url_for(f'admin.{role_type}'))
        elif action == 'deactivate':
            user_data.is_active = False
            db.session.commit()
            flash(f'{user_data.first_name} is now Deactivated', 'danger')
            return redirect(url_for(f'admin.{role_type}'))
        elif action == 'block':
            user_data.is_blocked = True
            db.session.commit()
            flash(f'{user_data.first_name} is now Blacklisted', 'danger')
            return redirect(url_for(f'admin.{role_type}'))
        elif action == 'unblock':
            user_data.is_blocked = False
            db.session.commit()
            flash(f'{user_data.first_name} is now Unblacklisted', 'success')
            return redirect(url_for(f'admin.{role_type}'))
        else:
            flash('Invalid Action', 'error')
            return redirect(url_for(f'admin.{role_type}'))




@admin_bp.route('/trek')
@login_required
@role_required('admin')
def trek():
    pass
    # treks = Trek.query.all()
    # form = AddTrekForm()
    # return render_template('admin/treks.html',
    #                        page = 'Treks'
    #                        treks = treks, form = form,
    #                        type = 'treks')


@admin_bp.route('/booking')
@login_required
@role_required('admin')
def booking():
    admin_id = current_user.id
    admin_data = User.query.filter_by(id = admin_id).first()
    return render_template('admin/booking.html',page = 'booking', first_name = admin_data.first_name,
                           email = admin_data.email,
                           role = admin_data.role)

@admin_bp.route('/history')
@login_required
@role_required('admin')
def history():
    admin_id = current_user.id
    admin_data = User.query.filter_by(id = admin_id).first()
    return render_template('admin/history.html',
                           page = 'history', first_name = admin_data.first_name,
                           email = admin_data.email,
                           role = admin_data.role)




@admin_bp.route('/profile')
@login_required
@role_required('admin')
def profile():
    admin_id = current_user.id
    admin_data = User.query.filter_by(id = admin_id).first()
    return render_template('admin/profile.html',page = 'Profile', first_name = admin_data.first_name,
                           email = admin_data.email,
                           role = admin_data.role)


