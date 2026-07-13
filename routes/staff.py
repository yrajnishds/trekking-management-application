from flask import Blueprint, render_template, redirect, url_for
from flask import request, flash
from flask_login import current_user, login_required
from sqlalchemy import or_, desc

from models import db
from models.model import User, Trek
from models.model import Booking
from routes.decorators import role_required

from forms.trek_form import TrekActionForm, TrekUpdateForm
from forms.user_form import ProfileUpdateForm

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

    # ========== Booking ========
    
    booking = Booking.query.join(Booking.trek).filter(
        Trek.staff_id == current_user.id,

    )
    booking_total = booking.count()
    booking_pending = booking.filter(Booking.status == 'pending').count()
    booking_approved = booking.filter(Booking.status == 'approved').count()
    booking_requested = booking.filter(Booking.status == 'requested').count()
    booking_completed = booking.filter(Booking.status == 'completed').count()
    booking_cancelled = booking.filter(Booking.status == 'cancelled').count()
    booking_rejected = booking.filter(Booking.status == 'rejected').count()

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
    trek_total = Trek.query.filter(
        Trek.staff_id == current_user.id
    ).count()
    trek_pending = Trek.query.filter(Trek.staff_id == current_user.id, Trek.trek_status == 'pending').count()
    trek_approved = Trek.query.filter(Trek.staff_id == current_user.id, Trek.trek_status == 'approved').count()
    trek_ongoing = Trek.query.filter(Trek.staff_id == current_user.id, Trek.trek_status == 'ongoing').count()
    trek_open = Trek.query.filter(Trek.staff_id == current_user.id, Trek.trek_status == 'open').count()
    trek_closed = Trek.query.filter(Trek.staff_id == current_user.id, Trek.trek_status == 'closed').count()
    trek_completed = Trek.query.filter(Trek.staff_id == current_user.id, Trek.trek_status == 'completed').count()
    trek_cancelled = Trek.query.filter(Trek.staff_id == current_user.id, Trek.trek_status == 'cancelled').count()

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
        'staff/dashboard.html',
        page = 'dashboard',
        booking_data = booking_data,
        trek_data = trek_data
    )

@staff_bp.route('/trek')
@login_required
@role_required('staff')
def trek():
    trek_action_form = TrekActionForm()
    trek_action_form.trek_action.choices = [('', '---Choose Status---')] +  [('open', 'Open'), ('closed', 'Closed'), ('completed', 'Completed')]
    user_id = current_user.id
    treks = Trek.query.filter_by(staff_id = user_id).all()
    return render_template('staff/trek.html',
                           page = 'trek',
                           treks = treks,
                           trek_action_form = trek_action_form)

@staff_bp.route('/trek/<string:code>', methods = ['GET', 'POST'])
@login_required
@role_required('staff')
def staff_trek_action_status(code):
    if request.method == "POST":
        trek = Trek.query.filter_by(trek_code = code).first()
        if not trek:
            flash('Invalid Trek Code', 'error')
            return redirect(url_for('staff.trek'))
        
        trek_action = request.form.get('trek_action')
        trek.trek_status = trek_action
        db.session.commit()
        flash(f'Trek Status for trek code {code} changed to {trek_action}', 'info')
        return redirect(url_for('staff.trek'))

    return redirect(url_for('staff.trek'))


@staff_bp.route('/edit-trek/<string:code>/update', methods = ['GET', 'POST'])
@login_required
@role_required('staff')
def edit_trek(code):

    trek = Trek.query.filter_by(trek_code = code).first()
    form = TrekUpdateForm()

    form.trek_code.choices = [(trek.trek_code, trek.trek_code)]
    form.trek_name.choices = [(trek.trek_name, trek.trek_name)]

    return render_template('staff/edit_trek.html',
                           form = form,
                           trek = trek)




@staff_bp.route('/trek/details/update', methods = ['GET', 'POST'])
@login_required
@role_required('staff')
def update_trek_details():
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

        return redirect(url_for('staff.trek'))

    else:
        return redirect(url_for('staff.trek'))




@staff_bp.route('/booking')
@login_required
@role_required('staff')
def booking():
    bookings = db.session.query(Booking).join(Booking.trek).filter(
        Trek.staff_id == current_user.id,
        Booking.status != 'completed', 
        Booking.status != 'cancelled', 
        Booking.status != 'rejected'
    ).order_by(
        desc(Booking.booking_date),
        desc(Booking.id)
    ).all()
    total = db.session.query(Booking).join(Booking.trek).filter(
        Trek.staff_id == current_user.id,
        
            Booking.status != 'completed', 
            Booking.status != 'cancelled', 
            Booking.status != 'rejected', 
        
    ).count()

    # total = Booking.query.join(Booking.trek).filter(Trek.staff_id == current_user.id).count()

    pending = Booking.query.filter_by(status = 'pending').join(Booking.trek).filter(Trek.staff_id == current_user.id).count()
    approved = Booking.query.filter_by(status = 'approved').join(Booking.trek).filter(Trek.staff_id == current_user.id).count()
    rejected = Booking.query.filter_by(status = 'rejected').join(Booking.trek).filter(Trek.staff_id == current_user.id).count()
    cancelled = Booking.query.filter_by(status = 'cancelled').join(Booking.trek).filter(Trek.staff_id == current_user.id).count()
    requested = Booking.query.filter_by(status = 'requested').join(Booking.trek).filter(Trek.staff_id == current_user.id).count()
    completed = Booking.query.filter_by(status = 'completed').join(Booking.trek).filter(Trek.staff_id == current_user.id).count()
    return render_template('staff/booking.html',page = 'booking',
                           bookings = bookings,
                           total = total,
                           approved = approved,
                           pending = pending,
                           rejected = rejected,
                           cancelled = cancelled,
                           requested = requested,
                           completed = completed)


@staff_bp.route('/booking/<int:id>/<string:action>/<int:trek_id>/<string:status>', methods = ['GET', 'POST'])
@login_required
@role_required('staff')
def staff_booking_action(id, trek_id, action, status):
    if request.method == 'POST':
        booking = Booking.query.filter_by(id=id).first()
        trek = Trek.query.filter_by(id=trek_id).first()

        
        if not booking or not trek:
            flash('Booking or Trek record not found.', 'danger')
            return redirect(url_for('staff.booking'))

        if action == 'rejected' and status == 'pending':
            booking.status = action                       
            
            db.session.add(booking)
            db.session.add(trek)
            db.session.commit()

            flash('Booking Rejection Successful', 'success')
            return redirect(url_for('staff.booking'))

        elif action == 'approved':
            booking.status = action           
            trek.booked_slots += 1     
            
            db.session.add(booking)
            db.session.add(trek)
            db.session.commit()
            
            flash('Booking Approval Successful', 'success')
            return redirect(url_for('staff.booking'))

        elif action == 'rejected':
            booking.status = action
            trek.booked_slots -= 1
            
            db.session.add(booking)
            db.session.add(trek)
            db.session.commit()
            
            flash('Booking Rejection Successful', 'danger')
            return redirect(url_for('staff.booking'))
        
        elif action == 'cancelled':
            booking.status = action            
            trek.booked_slots -= 1             
            
            db.session.add(booking)
            db.session.add(trek)
            db.session.commit()
            
            flash('Booking Cancellation Successful', 'danger')
            return redirect(url_for('staff.booking'))
        elif action == 'completed':
            booking.status = action                      
            
            db.session.add(booking)
            db.session.commit()
            
            flash('Trek Completed', 'success')
            return redirect(url_for('staff.booking'))
            
        else:
            flash('Invalid Action', 'warning')
            return redirect(url_for('staff.booking'))


@staff_bp.route('/history')
@login_required
@role_required('staff')
def history():
    bookings = db.session.query(Booking).join(Booking.trek).filter(
        Trek.staff_id == current_user.id,
        or_(
            Booking.status == 'completed', 
            Booking.status == 'cancelled', 
            Booking.status == 'rejected', 
        )
    ).order_by(
        desc(Booking.booking_date),
        desc(Booking.id)
    ).all()

    total = db.session.query(Booking).join(Booking.trek).filter(
        Trek.staff_id == current_user.id,
        or_(
            Booking.status == 'completed', 
            Booking.status == 'cancelled', 
            Booking.status == 'rejected', 
        )
    ).count()

    rejected = Booking.query.filter_by(status = 'rejected').join(Booking.trek).filter(Trek.staff_id == current_user.id).count()
    cancelled = Booking.query.filter_by(status = 'cancelled').join(Booking.trek).filter(Trek.staff_id == current_user.id).count()
    completed = Booking.query.filter_by(status = 'completed').join(Booking.trek).filter(Trek.staff_id == current_user.id).count()
    return render_template('staff/history.html',page = 'history',
                           bookings = bookings,
                           total = total,
                           rejected = rejected,
                           cancelled = cancelled,
                           completed = completed)




@staff_bp.route('/profile')
@login_required
@role_required('staff')
def profile():
    update_form = ProfileUpdateForm()
    return render_template('staff/profile.html',page = 'profile',
                           update_form = update_form)

@staff_bp.route('/profile/update', methods = ['GET', 'POST'])
@login_required
@role_required('staff')
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
            user_data.staff_profile.contact = update_form.contact.data
            flash('Contact Details Update Successful', 'success')
        if update_form.dob.data:
            user_data.staff_profile.dob = update_form.dob.data
            flash('Date Of Birth Update Successful', 'success')
        if update_form.bio.data:
            user_data.staff_profile.bio = update_form.bio.data
            flash('About Update Successful', 'success')
        if update_form.password.data:
            user_data.password = update_form.password.data
            flash('Password Update Successful', 'success')
        db.session.commit()
        flash('Profile Updated Successfully', 'success')
        return redirect(url_for(f'{current_user.role}.profile'))
    return render_template('staff/edit_profile.html', update_form = update_form)


@staff_bp.route('/search', methods = ['GET', 'POST'])
@login_required
@role_required('staff')
def search():

    trek_action_form = TrekActionForm()
    trek_action_form.trek_action.choices = [('', '---Choose Status---')] +  [('open', 'Open'), ('closed', 'Closed'), ('completed', 'Completed')]
    from search import staff_search
    search = request.args.get('search', '').strip()
    if not search:
        return redirect(url_for('staff.staff'))
    results = staff_search(current_user.id, search)
    return render_template(
        'staff/search.html',
        search = search,
        results = results,
        trek_action_form = trek_action_form
    )