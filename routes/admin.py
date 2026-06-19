from flask import Blueprint,  render_template, redirect, url_for
from flask import flash, request
from flask_login import current_user, login_required
from models.model import User, Trek
from routes.decorators import role_required
from models import db
from forms.user_form import UsersAddForm, ProfileUpdateForm
from forms.trek_form import TrekAddForm, AssignStaffForm

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
    form = UsersAddForm()
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
    trekkers = User.query.filter_by(role = 'staff').all()
    form = UsersAddForm()
    total = User.query.filter_by(role = 'staff').count()
    approved = User.query.filter_by(role = 'staff', approval_status = 'approved').count()
    pending = total - approved
    active = User.query.filter_by(role = 'staff', is_active = True).count()
    inactive = total - active
    blacklisted = User.query.filter_by(role = 'staff', is_blocked = True).count()
    unblacklisted = total - blacklisted

    return render_template('admin/staff.html',
                           page = 'trekkers',
                           users = trekkers, form = form,
                           role_type = 'staff',
                           total = total,
                           approved = approved,
                           pending = pending,
                           active = active,
                           inactive = inactive,
                           blacklisted = blacklisted,
                           unblacklisted = unblacklisted)


@admin_bp.route('/add-user/<string:role_type>', methods = ['GET', 'POST'])
@login_required
@role_required('admin')
def add_user(role_type):
    form = UsersAddForm()
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
        if role_type == 'staff':
            trek_data = Trek.query.filter_by(assigned_staff_id = id).all()
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
            user_data.is_active = False
            user_data.approval_status = 'pending'
            if trek_data:
                for trek in trek_data:
                    trek.assigned_staff_id = None
                    db.session.commit()
            db.session.commit()
            flash(f'{user_data.first_name} is now Blacklisted', 'danger')
            return redirect(url_for(f'admin.{role_type}'))
        elif action == 'unblock':
            user_data.is_blocked = False
            user_data.is_active = True
            user_data.approval_status = 'approved'
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

    form = TrekAddForm()
    treks = Trek.query.all()
    total_treks = Trek.query.count()
    approved = Trek.query.filter_by(trek_status = 'approved').count()
    pending = Trek.query.filter_by(trek_status = 'pending').count()
    open = Trek.query.filter_by(trek_status = 'open').count()
    closed = Trek.query.filter_by(trek_status = 'closed').count()
    completed = Trek.query.filter_by(trek_status = 'completed').count()
    easy = Trek.query.filter_by(difficulty = 'easy').count()
    moderate = Trek.query.filter_by(difficulty = 'moderate').count()
    hard = Trek.query.filter_by(difficulty = 'hard').count()


    assign_staff_form = AssignStaffForm()
    staffs = User.query.filter_by(role = 'staff', approval_status = 'approved', is_active = True, is_blocked = False).all()
    # if staffs:
    assign_staff_form.assigned_staff.choices = [('', '---Choose Staff---')] + [(staff.id, staff.email) for staff in staffs]
    

    return render_template('admin/trek.html',
                           page = 'Treks',
                           treks = treks,
                           form = form,
                           total_treks = total_treks,
                           approved = approved,
                           pending = pending,
                           open = open,
                           closed = closed,
                           completed = completed,
                           easy = easy,
                           moderate = moderate,
                           hard = hard,
                           assign_staff_form = assign_staff_form
                           )

@admin_bp.route('/add-trek', methods = ['GET', 'POST'])
@login_required
@role_required('admin')
def add_trek():
    form = TrekAddForm()
    if form.validate_on_submit():
        trek = Trek.query.filter_by(trek_id = form.trek_id.data).first()
        if trek:
            flash(f'Trek with id {form.trek_id.data} Already exists..', 'error')
            flash(f'Trek Name is {trek.trek_name}.', 'info')
            return redirect(url_for('admin.trek'))
        else:
            new_trek = Trek(
                trek_id = form.trek_id.data.strip().lower(),
                trek_name = form.trek_name.data.strip().lower(),
                location = form.location.data.strip().lower(),
                difficulty = form.difficulty.data.strip().lower(),
                duration = form.duration.data,
                no_of_slots = form.no_of_slots.data,
                trek_status = form.trek_status.data.strip().lower(),
                start_date = form.start_date.data,
                end_date = form.end_date.data,
                price = form.price.data,
                description = form.description.data.strip().lower()
            )
            db.session.add(new_trek)
            db.session.commit()
            flash(f'Trek with Id: {form.trek_id.data} Created Successfully', 'success')
            flash(f'Trek Name: {form.trek_name.data}', 'info')
            return redirect(url_for('admin.trek'))

@admin_bp.route('/trek/<string:trek_id>/<string:action>', methods = ['GET', 'POST'])
@login_required
@role_required('admin')
def admin_trek_action(trek_id, action):

    if request.method == "POST":
        staff_id = request.form.get('assigned_staff')
        staffs = User.query.filter_by(id = staff_id).first()
        trek = Trek.query.filter_by(trek_id = trek_id).first()
        if not trek:
            flash('Invalid Trek Id', 'error')
            return redirect(url_for('admin.trek'))
        if action == 'assign_staff' or action == 'change_staff':
            trek.assigned_staff_id = staff_id
            db.session.commit()
            flash(f'staff {staffs.email} is assigned for {trek.trek_id} successfully', 'success')
            return redirect(url_for('admin.trek'))
        


    pass



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
    update_form = ProfileUpdateForm()
    admin_data = User.query.filter_by(id = admin_id).first()
    return render_template('admin/profile.html',page = 'Profile',
                           update_form = update_form)

@admin_bp.route('/profile/update', methods = ['GET', 'POST'])
@login_required
@role_required('admin')
def update_profile():
    update_form = ProfileUpdateForm()
    if update_form.validate_on_submit():
        user_data = User.query.filter_by(id = current_user.id).first()
        if update_form.name.data:
            name = update_form.name.data.strip().split()
            if len(name) != 1:
                first_name = name[0].lower()
                last_name = " ".join(name[1:]).lower()
            else:
                first_name = name[0].lower()
                last_name = None
            user_data.first_name = first_name
            flash('Name Chnaged Successfully', 'success')
            user_data.last_name = last_name
        if update_form.contact.data:
            user_data.contact = update_form.contact.data
            flash('Contact Details Update Successful', 'success')
        if update_form.dob.data:
            user_data.dob = update_form.dob.data
            flash('Date Of Birth Update Successful', 'success')
        if update_form.bio.data:
            user_data.bio = update_form.bio.data
            flash('About Update Successful', 'success')
        if update_form.password.data:
            user_data.password_hash = update_form.password.data
            flash('Password Update Successful', 'success')
        db.session.commit()
        flash('Profile Updated Successfully', 'success')
        return redirect(url_for(f'{current_user.role}.profile'))
    return render_template('components/update_profile.html', update_form = update_form)


