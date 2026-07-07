from flask import Blueprint,  render_template, redirect, url_for
from flask import flash, request
from flask_login import current_user, login_required
from models.model import User, Trek, Booking
from models.model import TrekkerProfile, StaffProfile
from routes.decorators import role_required
from models import db
from forms.user_form import UsersAddForm, ProfileUpdateForm
from forms.trek_form import TrekAddForm, AssignStaffForm, TrekActionForm
from forms.user_form import TrekkerRegisterForm

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
    trekkers_data = User.query.filter_by(role = 'trekker').all()
    form = UsersAddForm()
    form.role.choices = [('trekker', 'Trekker')]

    total = User.query.filter_by(role = 'trekker').count()
    approved = User.query.filter_by(role = 'trekker', is_approved = True).count()
    pending = total - approved
    active = User.query.filter_by(role = 'trekker', is_active = True).count()
    inactive = total - active
    blacklisted = User.query.filter_by(role = 'trekker', is_blocked = True).count()
    unblacklisted = total - blacklisted

    return render_template('admin/trekker.html',
                           page = 'trekkers',
                           role_type = 'trekker',
                           users = trekkers, form = form,
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
    form = UsersAddForm()
    form.role.choices = [('staff', 'Staff')]
    total = User.query.filter_by(role = 'staff').count()
    approved = User.query.filter_by(role = 'staff', is_approved = True).count()
    pending = total - approved
    active = User.query.filter_by(role = 'staff', is_active = True).count()
    inactive = total - active
    blacklisted = User.query.filter_by(role = 'staff', is_blocked = True).count()
    unblacklisted = total - blacklisted

    return render_template('admin/staff.html',
                           page = 'staffs',
                           users = staffs, form = form,
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
            
            flash(f'{user.role.capitalize()} With this email already exits', 'error')

            return redirect(url_for(f'admin.{role_type}'))
            
        else:
            name = form.name.data.split()
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
                is_approved = True
            else:
                is_approved = False
            new_user = User(first_name = first_name,
                            last_name = last_name,
                            email = email,
                            password = password,
                            role = role,
                            is_approved = is_approved)


            if new_user.role == "staff":
                new_user.staff_profile = StaffProfile()

            elif new_user.role == "trekker":
                new_user.trekker_profile = TrekkerProfile()


            db.session.add(new_user)
            db.session.commit()
            if role == 'trekker':            
                flash(f'Account Created Successful for {first_name}', 'success')
                return redirect(url_for(f'admin.{role_type}'))
            else:
                flash(f'Account Registration Successful for {first_name}', 'success')
                flash(f'Now You Can Update {role.capitalize()} Approval Status', 'info')
                return redirect(url_for(f'admin.{role_type}'))
    else:
        return redirect(url_for(f'admin.{role_type}'))




@admin_bp.route('/<string:role_type>/<int:id>/<string:action>', methods = ['GET', 'POST'])
@login_required
@role_required('admin')
def admin_action(role_type, id, action):

    if request.method == 'POST':
        user_data = User.query.get_or_404(id)
        if role_type == 'staff':
            trek_data = Trek.query.filter_by(staff_id = id).all()
        if not user_data:
            flash('Invalid Id', 'error')
            return redirect(url_for(f'admin.{role_type}'))
        if action == 'approved':
            user_data.is_approved = True
            db.session.commit()
            flash(f'Now Approval for {user_data.first_name} changed to {action}', 'success')
            return redirect(url_for(f'admin.{role_type}'))
        elif action == 'pending':
            user_data.is_approved = False
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
            user_data.is_approved = False
            if role_type == 'staff':
                if trek_data:
                    for trek in trek_data:
                        trek.assigned_staff_email = None
                        db.session.commit()
            db.session.commit()
            flash(f'{user_data.first_name} is now Blacklisted', 'danger')
            return redirect(url_for(f'admin.{role_type}'))
        elif action == 'unblock':
            user_data.is_blocked = False
            user_data.is_active = True
            user_data.is_approved = True
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
    total_treks = len(treks)
    approved = Trek.query.filter_by(trek_status = 'approved').count()
    pending = Trek.query.filter_by(trek_status = 'pending').count()
    open = Trek.query.filter_by(trek_status = 'open').count()
    closed = Trek.query.filter_by(trek_status = 'closed').count()
    completed = Trek.query.filter_by(trek_status = 'completed').count()


    assign_staff_form = AssignStaffForm()

    staffs = User.query.filter_by(role = 'staff', is_approved = True, is_active = True, is_blocked = False).all()
    # if staffs:
    assign_staff_form.assigned_staff.choices = [('', '---Choose Staff---')] + [(staff.id, staff.email) for staff in staffs]
    
    trek_action_form = TrekActionForm()
    trek_action_form.trek_action.choices = [('', '---Choose Status---')] +  [('pending', 'Pending'), ('approved', 'Approved'), ('open', 'Open'), ('closed', 'Closed'), ('completed', 'Completed'), ('cancelled', 'Cancelled')]

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
                           assign_staff_form = assign_staff_form,
                           trek_action_form = trek_action_form
                           )

@admin_bp.route('/add-trek', methods = ['GET', 'POST'])
@login_required
@role_required('admin')
def add_trek():
    form = TrekAddForm()
    if form.validate_on_submit():
        trek = Trek.query.filter_by(trek_code = form.trek_code.data).first()
        if trek:
            flash(f'Trek with code "{form.trek_code.data}" Already exists..', 'error')
            flash(f'Trek Name is {trek.trek_name}.', 'info')
            return redirect(url_for('admin.trek'))
        else:
            new_trek = Trek(
                trek_code = form.trek_code.data.strip().lower(),
                trek_name = form.trek_name.data.strip().lower(),
                location = form.location.data.strip().lower(),
                difficulty = form.difficulty.data.strip().lower(),
                duration = form.duration.data,
                slots = form.no_of_slots.data,
                trek_status = form.trek_status.data.strip().lower(),
                start_date = form.start_date.data,
                end_date = form.end_date.data,
                price = form.price.data,
                description = form.description.data.strip().lower()
            )
            db.session.add(new_trek)
            db.session.commit()
            flash(f'Trek with Code: {form.trek_code.data} Created Successfully', 'success')
            flash(f'Trek Name: {form.trek_name.data}', 'info')
            return redirect(url_for('admin.trek'))

@admin_bp.route('/trek/<string:code>/<string:action>', methods = ['GET', 'POST'])
@login_required
@role_required('admin')
def admin_trek_action(code, action):

    if request.method == "POST":
        staff_id = request.form.get('assigned_staff')
        staffs = User.query.filter_by(id = staff_id).first()
        trek = Trek.query.filter_by(trek_code = code).first()
        if not trek:
            flash('Invalid Trek Code', 'error')
            return redirect(url_for('admin.trek'))
        if action == 'assign_staff' or action == 'change_staff':
            trek.staff_id = staff_id
            staffs.id = staff_id
            

            db.session.commit()
            flash(f'staff {staffs.id} is assigned for {trek.trek_code} successfully', 'success')
            return redirect(url_for('admin.trek'))
        


@admin_bp.route('/trek/<string:code>', methods = ['GET', 'POST'])
@login_required
@role_required('admin')
def admin_trek_action_status(code):
    if request.method == "POST":
        trek = Trek.query.filter_by(trek_code = code).first()
        if not trek:
            flash('Invalid Trek Code', 'error')
            return redirect(url_for('admin.trek'))
        
        trek_action = request.form.get('trek_action')
        trek.trek_status = trek_action
        db.session.commit()
        flash(f'Trek Status for trek code {code} changed to {trek_action}', 'info')
        return redirect(url_for('admin.trek'))




@admin_bp.route('/booking')
@login_required
@role_required('admin')
def booking():
    bookings = Booking.query.all()
    total = Booking.query.count()
    pending = Booking.query.filter_by(status = 'pending').count()
    approved = Booking.query.filter_by(status = 'approved').count()
    rejected = Booking.query.filter_by(status = 'rejected').count()
    cancelled = Booking.query.filter_by(status = 'cancelled').count()
    requested = Booking.query.filter_by(status = 'requested').count()
    return render_template('admin/booking.html',page = 'booking',
                           bookings = bookings,
                           total = total,
                           approved = approved,
                           pending = pending,
                           rejected = rejected,
                           cancelled = cancelled,
                           requested = requested)


@admin_bp.route('/booking/<int:id>/<string:action>/<int:trek_id>/<string:status>', methods = ['GET', 'POST'])
@login_required
@role_required('admin')
def admin_booking_action(id, trek_id, action, status):
    if request.method == 'POST':
        booking = Booking.query.filter_by(id=id).first()
        trek = Trek.query.filter_by(id=trek_id).first()

        
        if not booking or not trek:
            flash('Booking or Trek record not found.', 'danger')
            return redirect(url_for('admin.booking'))

        if action == 'rejected' and status == 'pending':
            booking.status = action                       
            
            db.session.add(booking)
            db.session.add(trek)
            db.session.commit()

            flash('Booking Rejection Successful', 'success')
            return redirect(url_for('admin.booking'))

        elif action == 'approved':
            booking.status = action           
            trek.booked_slots += 1     
            
            db.session.add(booking)
            db.session.add(trek)
            db.session.commit()
            
            flash('Booking Approval Successful', 'success')
            return redirect(url_for('admin.booking'))

        elif action == 'rejected':
            booking.status = action
            trek.booked_slots -= 1
            
            db.session.add(booking)
            db.session.add(trek)
            db.session.commit()
            
            flash('Booking Rejection Successful', 'danger')
            return redirect(url_for('admin.booking'))
        elif action == 'cancelled':
            booking.status = action            
            trek.booked_slots -= 1             
            
            db.session.add(booking)
            db.session.add(trek)
            db.session.commit()
            
            flash('Booking Cancellation Successful', 'danger')
            return redirect(url_for('admin.booking'))
            
        else:
            flash('Invalid Action', 'warning')
            return redirect(url_for('admin.booking'))


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


