from flask import Blueprint, render_template, redirect, url_for
from flask import request, session, flash
from flask_login import current_user, login_required
from models import db
from models.model import User, Trek, Booking
from routes.decorators import role_required
from forms.trek_form import TrekBookForm
from forms.user_form import ProfileUpdateForm
from sqlalchemy import or_



trekker_bp = Blueprint('trekker', __name__)


@trekker_bp.route('/trekker')
@login_required
@role_required('trekker')
def trekker():
    return redirect(url_for('trekker.dashboard'))

@trekker_bp.route('/dashboard')
@login_required
@role_required('trekker')
def dashboard():

# ========== Booking ========
    booking_total = Booking.query.count()
    booking_pending = Booking.query.filter(Booking.trekker_id == current_user.id, Booking.status == 'pending').count()
    booking_approved = Booking.query.filter(Booking.trekker_id == current_user.id, Booking.status == 'approved').count()
    booking_requested = Booking.query.filter(Booking.trekker_id == current_user.id, Booking.status == 'requested').count()
    booking_rejected = Booking.query.filter(Booking.trekker_id == current_user.id, Booking.status == 'rejected').count()
    booking_completed = Booking.query.filter(Booking.trekker_id == current_user.id, Booking.status == 'completed').count()
    booking_cancelled = Booking.query.filter(Booking.trekker_id == current_user.id, Booking.status == 'cancelled').count()

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
        or_(
            Trek.trek_status == 'open',
            Trek.trek_status == 'approved',
            Trek.trek_status == 'ongoing'
        )
    ).count()
    trek_coming = Trek.query.filter(Trek.trek_status == 'approved').count()
    trek_ongoing = Trek.query.filter(Trek.trek_status == 'ongoing').count()
    trek_open = Trek.query.filter(Trek.trek_status == 'open').count()

    trek_data = [
        {"title": "Total Trek", "value": trek_total, "color": "total"},
        {"title": "Coming Soon", "value": trek_coming, "color": "pending"},
        {"title": "Open", "value": trek_open, "color": "open"},
        {"title": "Ongoing", "value": trek_ongoing, "color": "ongoing"}
    ]

    return render_template(
        'trekker/dashboard.html',
        page = 'dashboard',
        trek_data = trek_data,
        booking_data = booking_data
    )


@trekker_bp.route('/trek')
@login_required
@role_required('trekker')
def trek():
    trekker_id = current_user.id
    trekker_data = User.query.filter_by(id = trekker_id).first()
    treks = Trek.query.all()
    return render_template('trekker/trek.html',
                           page = 'trek', first_name = trekker_data.first_name,
                           email = trekker_data.email,
                           role = trekker_data.role,
                           treks = treks)

@trekker_bp.route('/booking')
@login_required
@role_required('trekker')
def booking():
    form = TrekBookForm()
    bookings = Booking.query.filter_by(trekker_id = current_user.id).all()
    total = Booking.query.filter_by(trekker_id = current_user.id).count()
    approved = Booking.query.filter_by(trekker_id = current_user.id, status='approved').count()
    pending = Booking.query.filter_by(trekker_id = current_user.id, status='pending').count()
    rejected = Booking.query.filter_by(trekker_id = current_user.id, status='rejected').count()
    cancelled = Booking.query.filter_by(trekker_id = current_user.id, status='cancelled').count()
    requested = Booking.query.filter_by(trekker_id = current_user.id, status='requested').count()
    completed = Booking.query.filter_by(trekker_id = current_user.id, status='completed').count()
    treks = Trek.query.filter_by(
        trek_status = 'open').filter(Trek.booked_slots < Trek.slots)
    form.trekker_id.choices = [(current_user.id, current_user.first_name)]
    form.trek_id.choices = [('', '---Choose Treks---')] + [(trek.id, trek.trek_code) for trek in treks]
    trek = Trek.query.all()
    return render_template('trekker/booking.html',
                           page = 'booking',
                           trek = trek,
                           form = form,
                           bookings = bookings,
                           total = total,
                           approved = approved,
                           pending = pending,
                           rejected = rejected,
                           cancelled = cancelled,
                           requested = requested,
                           completed = completed
                           )

@trekker_bp.route('/booking/', methods = ['GET', 'POST'])
@login_required
@role_required('trekker')
def trekker_booking_action():
    
    if request.method == 'POST':
        trekker_id = request.form.get('trekker_id')
        trek_id = request.form.get('trek_id')
        
        booking = Booking.query.filter(
            Booking.trekker_id == trekker_id, 
            Booking.trek_id == trek_id, 
            Booking.status.in_(['pending', 'approved']) 
        ).first()

        trek = Trek.query.filter_by(id = trek_id).first()
        if booking:
            flash(f'Already booking Exists For This Trek', 'info')
            flash(f'Booking Status is {booking.status}', 'info')
            return redirect(url_for('trekker.booking'))

        else:
            new_booking = Booking(
                trekker_id = trekker_id,
                trek_id = trek_id,
                amount_paid = trek.price
            )

            db.session.add(new_booking)
            db.session.commit()
            flash(f'Booking Successful', 'success')
            return redirect(url_for('trekker.booking'))
    else:
        return redirect(url_for('trekker.booking'))


@trekker_bp.route('/booking/<int:id>/<string:action>/<string:status>', methods=['GET', 'POST'])
@login_required
@role_required('trekker')
def booking_action(id, action, status):
    booking = Booking.query.filter_by(id=id).first()

    if not booking:
        flash('Booking not found.', 'danger')
        return redirect(url_for('trekker.booking'))

    if request.method == 'POST':
       
        if action == 'cancelled' and status == 'approved':
            booking.status = 'requested'
            db.session.commit()
            flash('Cancellation Request Sent...', 'info')
            return redirect(url_for('trekker.booking')) 
        
        elif action == 'cancelled' and status == 'pending':
            booking.status = 'cancelled'
            db.session.commit()
            flash('Booking Cancelled...', 'info')
            return redirect(url_for('trekker.booking')) 
        
   
    return redirect(url_for('trekker.booking'))



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


@trekker_bp.route('/profile')
@login_required
@role_required('trekker')
def profile():
    update_form = ProfileUpdateForm()
    return render_template('trekker/profile.html',page = 'Profile',
                           update_form = update_form)

@trekker_bp.route('/profile/edit', methods = ['GET', 'POST'])
@login_required
@role_required('trekker')
def edit_profile():
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
            user_data.trekker_profile.trekker_profile.contact = int(update_form.contact.data)
            flash('Contact Details Update Successful', 'success')
        if update_form.dob.data:
            user_data.trekker_profile.trekker_profile.dob = update_form.dob.data
            flash('Date Of Birth Update Successful', 'success')
        if update_form.bio.data:
            user_data.trekker_profile.bio = update_form.bio.data
            flash('About Update Successful', 'success')
        if update_form.password.data:
            user_data.password = update_form.password.data
            flash('Password Update Successful', 'success')
        db.session.commit()
        flash('Profile Updated Successfully', 'success')
        return redirect(url_for(f'{current_user.role}.profile'))
    return render_template('trekker/edit_profile.html', update_form = update_form)


@trekker_bp.route('/search')
@login_required
@role_required('trekker')
def search():
    trek_book_form = TrekBookForm
    from search import trekker_search
    search = request.args.get('search', '').strip()
    if not search:
        flash(f'Please enter the text to search...', 'info')
        return redirect(url_for('admin.admin'))
    results = trekker_search(current_user.id, search)
    return render_template(
        'trekker/search.html',
        search = search,
        results = results,
        trek_book_form = trek_book_form
    )