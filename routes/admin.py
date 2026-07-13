from flask import Blueprint,  render_template, redirect, url_for
from flask import flash, request
from flask_login import current_user, login_required
from models.model import User, Trek, Booking
from models.model import TrekkerProfile, StaffProfile
from routes.decorators import role_required
from models import db
from forms.user_form import UsersAddForm, ProfileUpdateForm
from forms.trek_form import TrekAddForm, AssignStaffForm, TrekActionForm, TrekUpdateForm
from sqlalchemy import desc, asc, or_

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

# ========== Trekker ========
    trekker_total = User.query.filter(User.role == 'trekker').count()
    trekker_inactive = User.query.filter(User.role == 'trekker', User.is_active == False).count()
    trekker_pending = User.query.filter(User.role == 'trekker', User.is_approved == False).count()
    trekker_blacklisted = User.query.filter(User.role == 'trekker', User.is_blocked == True).count()
    trekker_data = [
        {"title": 'Total Trekker', 'value': trekker_total, "color": "total"},
        {"title": 'Active Trekker', 'value': trekker_total - trekker_inactive, "color": "active"},
        {"title": 'Pending Trekker', 'value': trekker_pending, "color": "pending"},
        {"title": 'Approved Trekker', 'value': trekker_total - trekker_pending, "color": "approved"},
        {"title": 'Inactive Trekker', 'value': trekker_inactive, "color": "inactive"},
        {"title": 'Blacklisted Trekker', 'value': trekker_blacklisted, "color": "blacklisted"},
    ]

# ========== Staff ========
    staff_total = User.query.filter(User.role == 'staff').count()
    staff_inactive = User.query.filter(User.role == 'staff', User.is_active == False).count()
    staff_pending = User.query.filter(User.role == 'staff', User.is_approved == False).count()
    staff_blacklisted = User.query.filter(User.role == 'staff', User.is_blocked == True).count()
    staff_data = [
        {"title": 'Total Staff', 'value': staff_total, "color": "total"},
        {"title": 'Active Staff', 'value': staff_total - staff_inactive, "color": "active"},
        {"title": 'Pending Staff', 'value': staff_pending, "color": "pending"},
        {"title": 'Approved Staff', 'value': staff_total - staff_pending, "color": "approved"},
        {"title": 'Inactive Staff', 'value': staff_inactive, "color": "inactive"},
        {"title": 'Blacklisted Staff', 'value': staff_blacklisted, "color": "blacklisted"},
    ]

# ========== Booking ========
    booking_total = Booking.query.count()
    booking_pending = Booking.query.filter(Booking.status == 'pending').count()
    booking_approved = Booking.query.filter(Booking.status == 'approved').count()
    booking_requested = Booking.query.filter(Booking.status == 'requested').count()
    booking_rejected = Booking.query.filter(Booking.status == 'rejected').count()
    booking_completed = Booking.query.filter(Booking.status == 'completed').count()
    booking_cancelled = Booking.query.filter(Booking.status == 'cancelled').count()

    booking_data = [
        {"title": "Total Booking", "value": booking_total, "color": "total"},
        {"title": "Pending", "value": booking_pending, "color": "pending"},
        {"title": "Approved", "value": booking_approved, "color": "approved"},
        {"title": "Cancellation Requests", "value": booking_requested, "color": "completed"},
        {"title": "Completed", "value": booking_completed, "color": "completed"},
        {"title": "Cancelled", "value": booking_cancelled, "color": "cancelled"},
        {"title": "Rejected", "value": booking_rejected, "color": "rejected"}
    ]

# =============== Trek ============
    trek_total = Trek.query.count()
    trek_pending = Trek.query.filter(Trek.trek_status == 'pending').count()
    trek_approved = Trek.query.filter(Trek.trek_status == 'approved').count()
    trek_ongoing = Trek.query.filter(Trek.trek_status == 'ongoing').count()
    trek_open = Trek.query.filter(Trek.trek_status == 'open').count()
    trek_closed = Trek.query.filter(Trek.trek_status == 'closed').count()
    trek_completed = Trek.query.filter(Trek.trek_status == 'completed').count()
    trek_cancelled = Trek.query.filter(Trek.trek_status == 'cancelled').count()

    trek_data = [
        {"title": "Total Trek", "value": trek_total, "color": "total"},
        {"title": "Pending", "value": trek_pending, "color": "pending"},
        {"title": "Approved", "value": trek_approved, "color": "approved"},
        {"title": "Open", "value": trek_open, "color": "open"},
        {"title": "Ongoing", "value": trek_ongoing, "color": "ongoing"},
        {"title": "Closed", "value": trek_closed, "color": "closed"},
        {"title": "Completed", "value": trek_completed, "color": "completed"},
        {"title": "Cancelled", "value": trek_cancelled, "color": "cancelled"}
    ]
    return render_template(
        'admin/dashboard.html',
        page = 'dashboard',
        add_trek_form = TrekAddForm(),
        trekker_data = trekker_data,
        staff_data = staff_data,
        trek_data = trek_data,
        booking_data = booking_data
    )



@admin_bp.route('/trekker')
@login_required
@role_required('admin')
def trekker():
    add_user_form = UsersAddForm()
    add_user_form.role.choices = [('trekker', 'Trekker')]

# ========== Trekker ========
    trekker_total = User.query.filter(
        User.role == 'trekker',
        User.is_active != False
    ).count()
    trekker_inactive = User.query.filter(User.role == 'trekker', User.is_active == False).count()
    trekker_pending = User.query.filter(User.role == 'trekker', User.is_approved == False).count()
    trekker_blacklisted = User.query.filter(User.role == 'trekker', User.is_blocked == True).count()
    trekker_data = [
        {"title": 'Total Trekker', 'value': trekker_total, "color": "total"},
        {"title": 'Active Trekker', 'value': (trekker_total - trekker_inactive), "color": "active"},
        {"title": 'Pending Trekker', 'value': trekker_pending, "color": "pending"},
        {"title": 'Approved Trekker', 'value': (trekker_total - trekker_pending), "color": "approved"},
        {"title": 'Blacklisted Trekker', 'value': trekker_blacklisted, "color": "blacklisted"},
    ]

    query = User.query.filter(
        User.role == 'trekker',
    )
    if request.method == 'GET':
        is_approved = request.args.get('is_approved', '')
        is_active = request.args.get('is_active', '')
        is_blocked = request.args.get('is_blocked', '')
        sort = request.args.get('sort', 'created_at')
        orderby = request.args.get('orderby', 'desc')
    # ==== Import filter ======
    from filter import user_filter, user_sort
    query = user_filter(query, is_approved=is_approved, is_active=is_active, is_blocked=is_blocked)
    query = user_sort(query, sort, orderby)
    trekkers = query.all()
    return render_template(
        'admin/trekker.html',
        page = 'trekker',
        role_type = 'trekker',
        users = trekkers,
        add_user_form = add_user_form,
        trekkers = trekkers,
        trekker_data = trekker_data
    )


@admin_bp.route('trekker/<int:trekker_id>')
@login_required
@role_required('admin')
def view_trekker(trekker_id):
    trekker_details = User.query.filter_by(id = trekker_id).first()
    booking_details = Booking.query.filter_by(trekker_id = trekker_id).all()
    return render_template(
        'admin/view_trekker.html',
        id = trekker_details.id,
        first_name = trekker_details.first_name,
        last_name = trekker_details.last_name,
        email = trekker_details.email,
        created_at = trekker_details.created_at,
        contact = trekker_details.trekker_profile.contact,
        dob = trekker_details.trekker_profile.dob,
        bio = trekker_details.trekker_profile.bio,
        booking_details = booking_details
    )


@admin_bp.route('/staff')
@login_required
@role_required('admin')
def staff():
    add_user_form = UsersAddForm()
    add_user_form.role.choices = [('staff', 'Staff')]

# ========== Staff ========
    staff_total = User.query.filter(
        User.role == 'staff',
        User.is_active != False
    ).count()
    staff_inactive = User.query.filter(User.role == 'staff', User.is_active == False).count()
    staff_pending = User.query.filter(User.role == 'staff', User.is_approved == False).count()
    staff_blacklisted = User.query.filter(User.role == 'staff', User.is_blocked == True).count()
    staff_approved = staff_total - staff_pending
    staff_active = staff_total - staff_inactive
    staff_data = [
        {"title": 'Total Staff', 'value': staff_total, "color": "total"},
        {"title": 'Active Staff', 'value': staff_active, "color": "active"},
        {"title": 'Pending Staff', 'value': staff_pending, "color": "pending"},
        {"title": 'Approved Staff', 'value': staff_approved, "color": "approved"},
        {"title": 'Blacklisted Staff', 'value': staff_blacklisted, "color": "blacklisted"},
    ]

    query = User.query.filter(
        User.role == 'staff',
    )
    if request.method == 'GET':
        is_approved = request.args.get('is_approved', '')
        is_active = request.args.get('is_active', '')
        is_blocked = request.args.get('is_blocked', '')
        sort = request.args.get('sort', 'created_at')
        orderby = request.args.get('orderby', 'desc')
    # ==== Import filter ======
    from filter import user_filter, user_sort
    query = user_filter(query, is_approved=is_approved, is_active=is_active, is_blocked=is_blocked)
    query = user_sort(query, sort, orderby)
    staffs = query.all()
    return render_template(
        'admin/staff.html',
        page = 'staff',
        role_type = 'staff',
        users = staffs,
        add_user_form = add_user_form,
        staffs = staffs,
        staff_data = staff_data
    )



@admin_bp.route('admin/<int:admin_id>')
@login_required
@role_required('admin')
def view_admin(admin_id):
    staff_details = User.query.filter_by(id = admin_id).first()
    # trek_details = Trek.query.filter_by(staff_id = id).all()
    return render_template(
        'admin/view_admin.html',
        id = staff_details.id,
        first_name = staff_details.first_name,
        last_name = staff_details.last_name,
        email = staff_details.email,
        created_at = staff_details.created_at,
        contact = staff_details.admin_profile.contact,
        dob = staff_details.admin_profile.dob,
        bio = staff_details.admin_profile.bio
    )
@admin_bp.route('staff/<int:staff_id>')
@login_required
@role_required('admin')
def view_staff(staff_id):
    staff_details = User.query.filter_by(id = staff_id).first()
    trek_details = Trek.query.filter_by(staff_id = staff_id).all()
    return render_template(
        'admin/view_staff.html',
        id = staff_details.id,
        first_name = staff_details.first_name,
        last_name = staff_details.last_name,
        email = staff_details.email,
        created_at = staff_details.created_at,
        contact = staff_details.staff_profile.contact,
        dob = staff_details.staff_profile.dob,
        bio = staff_details.staff_profile.bio,
        trek_details = trek_details
    )


@admin_bp.route('/add-user/<string:role_type>', methods = ['GET', 'POST'])
@login_required
@role_required('admin')
def add_user(role_type):
    
    
    add_user_form = UsersAddForm()
    if add_user_form.validate_on_submit():
        user = User.query.filter_by(email = add_user_form.email.data).first()
        if user:
            
            flash(f'{user.role.capitalize()} With this email already exits', 'error')

            return redirect(url_for(f'admin.{role_type}'))
            
        else:
            name = add_user_form.name.data.split()
            if len(name) != 1:
                first_name = name[0].lower()
                last_name = " ".join(name[1:]).lower()
            else:
                first_name = name[0].lower()
                last_name = None
            email = add_user_form.email.data
            password = add_user_form.password.data
            role = add_user_form.role.data
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
    return redirect(url_for(f'admin.{role_type}'))



@admin_bp.route('/trek')
@login_required
@role_required('admin')
def trek():

    trek_total = Trek.query.filter(
        Trek.trek_status != 'compeletd',
        Trek.trek_status != 'cancelled'
    ).count()
    trek_pending = Trek.query.filter(Trek.trek_status == 'pending').count()
    trek_approved = Trek.query.filter(Trek.trek_status == 'approved').count()
    trek_ongoing = Trek.query.filter(Trek.trek_status == 'ongoing').count()
    trek_open = Trek.query.filter(Trek.trek_status == 'open').count()
    trek_closed = Trek.query.filter(Trek.trek_status == 'closed').count()

    trek_data = [
        {"title": "Total Trek", "value": trek_total, "color": "total"},
        {"title": "Pending", "value": trek_pending, "color": "pending"},
        {"title": "Approved", "value": trek_approved, "color": "approved"},
        {"title": "Open", "value": trek_open, "color": "open"},
        {"title": "Ongoing", "value": trek_ongoing, "color": "ongoing"},
        {"title": "Closed", "value": trek_closed, "color": "closed"}
    ]

    query = Trek.query.filter(
        Trek.trek_status != 'completed',
        Trek.trek_status != 'cancelled',
    )
    if request.method == "GET":
        difficulty = request.args.get("difficulty")
        status = request.args.get("status")
        sort = request.args.get("sort", "created_at")
        orderby = request.args.get("orderby", "desc")
    #         # === Import filter function
        from filter import trek_filter, trek_sort
        query = trek_filter(query, difficulty, status)
        query = trek_sort(query, sort, orderby)
    treks = query.all()

    assign_staff_form = AssignStaffForm()

    staffs = User.query.filter_by(role = 'staff', is_approved = True, is_active = True, is_blocked = False).all()
    # if staffs:
    assign_staff_form.assigned_staff.choices = [('', '---Choose Staff---')] + [(staff.id, staff.email) for staff in staffs]
    
    trek_action_form = TrekActionForm()
    trek_action_form.trek_action.choices = [('', '---Choose Status---')] +  [('pending', 'Pending'), ('approved', 'Approved'), ('open', 'Open'), ('closed', 'Closed'), ('completed', 'Completed'), ('cancelled', 'Cancelled')]

    return render_template('admin/trek.html',
                           page = 'trek',
                           treks = treks,
                           add_trek_form = TrekAddForm(),
                           trek_data = trek_data,
                           assign_staff_form = assign_staff_form,
                           trek_action_form = trek_action_form
                           )

@admin_bp.route('/view-trek/<int:trek_id>')
@login_required
@role_required('admin')
def view_trek(trek_id):
    trek_details = Trek.query.filter_by(id = trek_id).first()
    
    assign_staff_form = AssignStaffForm()

    staffs = User.query.filter_by(role = 'staff', is_approved = True, is_active = True, is_blocked = False).all()
    # if staffs:
    assign_staff_form.assigned_staff.choices = [('', '---Choose Staff---')] + [(staff.id, staff.email) for staff in staffs]
    
    return render_template(
        'admin/view_trek.html',
        page = 'trek',
        assign_staff_form = assign_staff_form,
        id = trek_details.id,
        trek_code = trek_details.trek_code,
        trek_name = trek_details.trek_name,
        location = trek_details.location,
        difficulty = trek_details.difficulty,
        duration = trek_details.duration,
        start_date = trek_details.start_date,
        end_date = trek_details.end_date,
        trek_status = trek_details.trek_status,
        slots = trek_details.slots,
        booked_slots = trek_details.booked_slots,
        price = trek_details.price,
        description = trek_details.description,
        staff_id = trek_details.staff_id
    )

@admin_bp.route('/edit-trek/<int:trek_id>', methods = ['GET', 'POST'])
@login_required
@role_required('admin')
def edit_trek(trek_id):

    trek = Trek.query.filter_by(id = trek_id).first()
    form = TrekUpdateForm()

    form.trek_code.choices = [(trek.trek_code, trek.trek_code)]
    form.trek_name.choices = [(trek.trek_name, trek.trek_name)]

    return render_template('admin/edit_trek.html',
                           page = 'trek',
                           form = form,
                           trek = trek)




@admin_bp.route('/trek/details/update', methods = ['GET', 'POST'])
@login_required
@role_required('admin')
def edit_trek_details():
    form = TrekUpdateForm()
    if request.method == 'POST':
        trek_code = form.trek_code.data
        location = form.location.data
        difficulty = form.difficulty.data
        duration = form.duration.data
        no_of_slots = form.no_of_slots.data
        start_date = form.start_date.data
        end_date = form.end_date.data
        price = form.price.data
        description = form.description.data

        trek_detail = Trek.query.filter_by(trek_code = trek_code).first()

        if trek_detail:
            if location:
                trek_detail.location = location
            if difficulty:
                trek_detail.difficulty = difficulty
            if duration:
                trek_detail.duration = duration
            if no_of_slots:
                trek_detail.slots = no_of_slots
            if start_date:
                trek_detail.start_date = start_date
            if end_date:
                trek_detail.end_date = end_date
            if price:
                trek_detail.price = price
            if description:
                trek_detail.description = description
                
            db.session.commit() 

            flash(f'Trek Details Upadted Successful', 'success')

        return redirect(url_for('admin.trek'))

    else:
        return redirect(url_for('admin.trek'))



@admin_bp.route('/add-trek', methods = ['GET', 'POST'])
@login_required
@role_required('admin')
def add_trek():
    add_trek_form = TrekAddForm()

    if add_trek_form.validate_on_submit():
        trek = Trek.query.filter_by(trek_code = add_trek_form.trek_code.data).first()
        if trek:
            flash(f'Trek with code "{add_trek_form.trek_code.data}" Already exists..', 'danger')
            flash(f'Trek Name is {trek.trek_name}.', 'info')
            return redirect(url_for('admin.trek'))
        else:
            new_trek = Trek(
                trek_code = add_trek_form.trek_code.data.strip().lower(),
                trek_name = add_trek_form.trek_name.data.strip().lower(),
                location = add_trek_form.location.data.strip().lower(),
                difficulty = add_trek_form.difficulty.data.strip().lower(),
                duration = add_trek_form.duration.data,
                slots = add_trek_form.no_of_slots.data,
                trek_status = add_trek_form.trek_status.data.strip().lower(),
                start_date = add_trek_form.start_date.data,
                end_date = add_trek_form.end_date.data,
                price = add_trek_form.price.data,
                description = add_trek_form.description.data.strip().lower()
            )
            db.session.add(new_trek)
            db.session.commit()
            flash(f'Trek with Code: {add_trek_form.trek_code.data} Created Successfully', 'success')
            flash(f'Trek Name: {add_trek_form.trek_name.data}', 'info')
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
    if action == 'remove_staff':
        trek = Trek.query.filter_by(trek_code = code).first()
        trek.staff_id = None
        db.session.commit()
        flash('Assigned Staff Removed', 'info')
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
    booking_total = Booking.query.filter(
        Booking.status != 'compeletd',
        Booking.status != 'cancelled',
        Booking.status != 'rejected'
    ).count()
    booking_pending = Booking.query.filter(Booking.status == 'pending').count()
    booking_approved = Booking.query.filter(Booking.status == 'approved').count()
    booking_requested = Booking.query.filter(Booking.status == 'requested').count()

    booking_data = [
        {"title": "Total Booking", "value": booking_total, "color": "total"},
        {"title": "Pending", "value": booking_pending, "color": "pending"},
        {"title": "Approved", "value": booking_approved, "color": "approved"},
        {"title": "Cancellation Requests", "value": booking_requested, "requested": "primary"}
    ]
    
    query = Booking.query.filter(
        Booking.status != 'completed',
        Booking.status != 'rejected',
        Booking.status != 'cancelled',
    )
    if request.method == "GET":
        status = request.args.get("status")
        sort = request.args.get("sort", "booking_date")
        orderby = request.args.get("orderby", "desc")
    #         # === Import filter function
        from filter import booking_filter, booking_sort
        query = booking_filter(query, status)
        query = booking_sort(query, sort, orderby)
    bookings = query.all()
    
    return render_template('admin/booking.html',page = 'booking',
                           bookings = bookings,
                           booking_data = booking_data)



@admin_bp.route('/booking/trek/<int:trek_id>')
@login_required
@role_required('admin')
def view_booking(trek_id):
    booking_details = Booking.query.filter_by(trek_id = trek_id).all()

    return render_template(
        'admin/view_booking.html',
        page = 'bookings',
        booking_details = booking_details
    )



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

        elif action == 'complete':
            booking.status = action        
            
            
            db.session.add(booking)
            db.session.add(trek)
            db.session.commit()
            
            flash('Booking Completed Successful', 'success')
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


@admin_bp.route('/profile')
@login_required
@role_required('admin')
def profile():
    update_form = ProfileUpdateForm()
    return render_template('admin/profile.html',page = 'profile',
                           update_form = update_form)

@admin_bp.route('/profile/update', methods = ['GET', 'POST'])
@login_required
@role_required('admin')
def update_profile():
    update_form = ProfileUpdateForm()
    if update_form.validate_on_submit():
        user_data = User.query.filter_by(id = current_user.id).first()
        if update_form.first_name.data:
            user_data.first_name = update_form.first_name.data
            flash('First Name Changed Successfully', 'success')
        if update_form.last_name.data:
            user_data.last_name = update_form.last_name.data
            flash('Last Name Changed Successfully', 'success')
        if update_form.contact.data:
            user_data.admin_profile.contact = update_form.contact.data
            flash('Contact Details Update Successful', 'success')
        if update_form.dob.data:
            user_data.admin_profile.dob = update_form.dob.data
            flash('Date Of Birth Update Successful', 'success')
        if update_form.bio.data:
            user_data.admin_profile.bio = update_form.bio.data
            flash('About Update Successful', 'success')
        if update_form.password.data:
            user_data.password = update_form.password.data
            flash('Password Update Successful', 'success')
        db.session.commit()
        flash('Profile Updated Successfully', 'success')
        return redirect(url_for(f'{current_user.role}.profile'))
    return render_template(
        'admin/update_profile.html',
        page = 'profile',
        update_form = update_form
    )


@admin_bp.route('/history')
@login_required
@role_required('admin')
def history():

    # ============ Treks ==========
    trek_total = Trek.query.filter(
        or_(
            Trek.trek_status == 'compeletd',
            Trek.trek_status == 'cancelled',
        )
    ).count()
    trek_completed = Trek.query.filter(Trek.trek_status == 'completed').count()
    trek_cancelled = Trek.query.filter(Trek.trek_status == 'cancelled').count()
    trek_data = [
        {"title": "Total Trek", "value": trek_total, "color": "total"},
        {"title": "Completed", "value": trek_completed, "color": "completed"},
        {"title": "Cancelled", "value": trek_cancelled, "color": "cancelled"}
    ]

    # ================= Booking =====================
    booking_total = Booking.query.filter(
        or_(
            Booking.status == 'compeletd',
            Booking.status == 'cancelled',
            Booking.status == 'rejected'
        )
    ).count()
    booking_rejected = Booking.query.filter(Booking.status == 'rejected').count()
    booking_completed = Booking.query.filter(Booking.status == 'completed').count()
    booking_cancelled = Booking.query.filter(Booking.status == 'cancelled').count()

    booking_data = [
        {"title": "Total Booking", "value": booking_total, "color": "total"},
        {"title": "Completed", "value": booking_completed, "color": "completed"},
        {"title": "Cancelled", "value": booking_cancelled, "color": "cancelled"},
        {"title": "Rejected", "value": booking_rejected, "color": "rejected"}
    ]

    booking_query = Booking.query.filter(
        Booking.status != 'pending',
        Booking.status != 'approved',
        Booking.status != 'requested',
    )

    trek_query = Trek.query.filter(
        Trek.trek_status != 'open',
        Trek.trek_status != 'approved',
        Trek.trek_status != 'pending',
        Trek.trek_status != 'ongoing',
        Trek.trek_status != 'closed',
    )


    return render_template(
        'admin/history.html',
        page = 'history',
        booking_data = booking_data,
        trek_data = trek_data,
        bookings = booking_query.all(),
        treks = trek_query.all()
    )


@admin_bp.route('/history/booking')
@login_required
@role_required('admin')
def history_booking():

    query = Booking.query.filter(
        Booking.status != 'pending',
        Booking.status != 'approved',
        Booking.status != 'requested',
    )

    trek_query = Trek.query.filter(
        Trek.trek_status != 'open',
        Trek.trek_status != 'approved',
        Trek.trek_status != 'pending',
        Trek.trek_status != 'ongoing',
        Trek.trek_status != 'closed',
    )

    # ============ Treks ==========
    trek_total = Trek.query.filter(
        or_(
            Trek.trek_status == 'compeletd',
            Trek.trek_status == 'cancelled',
        )
    ).count()
    trek_completed = Trek.query.filter(Trek.trek_status == 'completed').count()
    trek_cancelled = Trek.query.filter(Trek.trek_status == 'cancelled').count()
    trek_data = [
        {"title": "Total Trek", "value": trek_total, "color": "total"},
        {"title": "Completed", "value": trek_completed, "color": "completed"},
        {"title": "Cancelled", "value": trek_cancelled, "color": "cancelled"}
    ]

    # ================= Booking =====================
    booking_total = Booking.query.filter(
        or_(
            Booking.status == 'compeletd',
            Booking.status == 'cancelled',
            Booking.status == 'rejected'
        )
    ).count()
    booking_rejected = Booking.query.filter(Booking.status == 'rejected').count()
    booking_completed = Booking.query.filter(Booking.status == 'completed').count()
    booking_cancelled = Booking.query.filter(Booking.status == 'cancelled').count()

    booking_data = [
        {"title": "Total Booking", "value": booking_total, "color": "total"},
        {"title": "Completed", "value": booking_completed, "color": "completed"},
        {"title": "Cancelled", "value": booking_cancelled, "color": "cancelled"},
        {"title": "Rejected", "value": booking_rejected, "color": "rejected"}
    ]
    
    if request.method == "GET":
        status = request.args.get("status")
        sort = request.args.get("sort", "booking_date")
        orderby = request.args.get("orderby", "desc")
    #         # === Import filter function
        from filter import booking_filter, booking_sort
        query = booking_filter(query, status)
        query = booking_sort(query, sort, orderby)
    bookings = query.all()

    return render_template(
        'admin/history.html',
        page = 'history',
        booking_data = booking_data,
        trek_data = trek_data,
        bookings = bookings,
        treks = trek_query.all()
    )


@admin_bp.route('/history/trek')
@login_required
@role_required('admin')
def history_trek():

    booking_query = Booking.query.filter(
        Booking.status != 'pending',
        Booking.status != 'approved',
        Booking.status != 'requested',
    )

    query = Trek.query.filter(
        Trek.trek_status != 'open',
        Trek.trek_status != 'approved',
        Trek.trek_status != 'pending',
        Trek.trek_status != 'ongoing',
        Trek.trek_status != 'closed',
    )

    # ============ Treks ==========
    trek_total = Trek.query.filter(
        or_(
            Trek.trek_status == 'compeletd',
            Trek.trek_status == 'cancelled',
        )
    ).count()
    trek_completed = Trek.query.filter(Trek.trek_status == 'completed').count()
    trek_cancelled = Trek.query.filter(Trek.trek_status == 'cancelled').count()
    trek_data = [
        {"title": "Total Trek", "value": trek_total, "color": "total"},
        {"title": "Completed", "value": trek_completed, "color": "completed"},
        {"title": "Cancelled", "value": trek_cancelled, "color": "cancelled"}
    ]

    # ================= Booking =====================
    booking_total = Booking.query.filter(
        or_(
            Booking.status == 'compeletd',
            Booking.status == 'cancelled',
            Booking.status == 'rejected'
        )
    ).count()
    booking_rejected = Booking.query.filter(Booking.status == 'rejected').count()
    booking_completed = Booking.query.filter(Booking.status == 'completed').count()
    booking_cancelled = Booking.query.filter(Booking.status == 'cancelled').count()

    booking_data = [
        {"title": "Total Booking", "value": booking_total, "color": "total"},
        {"title": "Completed", "value": booking_completed, "color": "completed"},
        {"title": "Cancelled", "value": booking_cancelled, "color": "cancelled"},
        {"title": "Rejected", "value": booking_rejected, "color": "rejected"}
    ]

    if request.method == "GET":
        difficulty = request.args.get("difficulty")
        status = request.args.get("status")
        sort = request.args.get("sort", "created_at")
        orderby = request.args.get("orderby", "desc")
    #         # === Import filter function
        from filter import trek_filter, trek_sort
        query = trek_filter(query, difficulty, status)
        query = trek_sort(query, sort, orderby)
    treks = query.all()

    return render_template(
        'admin/history.html',
        page = 'history',
        booking_data = booking_data,
        trek_data = trek_data,
        bookings = booking_query.all(),
        treks = treks
    )




@admin_bp.route('/search')
@login_required
@role_required('admin')
def search():

    assign_staff_form = AssignStaffForm()

    staffs = User.query.filter_by(role = 'staff', is_approved = True, is_active = True, is_blocked = False).all()
    # if staffs:
    assign_staff_form.assigned_staff.choices = [('', '---Choose Staff---')] + [(staff.id, staff.email) for staff in staffs]
    
    trek_action_form = TrekActionForm()
    trek_action_form.trek_action.choices = [('', '---Choose Status---')] +  [('pending', 'Pending'), ('approved', 'Approved'), ('open', 'Open'), ('closed', 'Closed'), ('completed', 'Completed'), ('cancelled', 'Cancelled')]

    from search import admin_search
    search = request.args.get("search", "").strip()
    if not search:
        flash(f'Please enter the text to search...', 'info')
        return redirect(url_for('admin.admin'))
    results = admin_search(search)
    return render_template(
        'admin/search.html',
        page = 'search',
        search = search,
        results = results,
        assign_staff_form = assign_staff_form,
        trek_action_form = trek_action_form
    )
