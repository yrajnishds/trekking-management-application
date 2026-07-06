from flask import Blueprint, render_template, redirect, url_for
from flask import request, flash
from flask_login import current_user, login_required

from models import db
from models.model import User, Trek
from models.model import Booking
from routes.decorators import role_required
from forms.trek_form import TrekActionForm

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
    user_id = current_user.id
    user_data = User.query.filter_by(id = user_id).first()
    return render_template('staff/dashboard.html',
                           page = 'dashboard', first_name = user_data.first_name,
                           email = user_data.email,
                           role = user_data.role)


@staff_bp.route('/trek')
@login_required
@role_required('staff')
def trek():
    trek_action_form = TrekActionForm()
    trek_action_form.trek_action.choices = [('', '---Choose Status---')] +  [('open', 'Open'), ('closed', 'Closed'), ('completed', 'Completed')]
    user_id = current_user.id
    treks = Trek.query.filter_by(staff_id = user_id).all()
    return render_template('staff/trek.html',
                           page = 'Assigned Treks',
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



@staff_bp.route('/booking')
@login_required
@role_required('staff')
def booking():
    bookings = Booking.query.join(Booking.trek).filter(Trek.staff_id == current_user.id).all()

    total = Booking.query.join(Booking.trek).filter(Trek.staff_id == current_user.id).count()

    pending = Booking.query.filter_by(status = 'pending').join(Booking.trek).filter(Trek.staff_id == current_user.id).count()
    approved = Booking.query.filter_by(status = 'approved').join(Booking.trek).filter(Trek.staff_id == current_user.id).count()
    rejected = Booking.query.filter_by(status = 'rejected').join(Booking.trek).filter(Trek.staff_id == current_user.id).count()
    cancelled = Booking.query.filter_by(status = 'cancelled').join(Booking.trek).filter(Trek.staff_id == current_user.id).count()
    requested = Booking.query.filter_by(status = 'requested').join(Booking.trek).filter(Trek.staff_id == current_user.id).count()
    return render_template('staff/booking.html',page = 'booking',
                           bookings = bookings,
                           total = total,
                           approved = approved,
                           pending = pending,
                           rejected = rejected,
                           cancelled = cancelled,
                           requested = requested)


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
    user_id = current_user.id
    user_data = User.query.filter_by(id = user_id).first()

    return render_template('staff/history.html',
                           page = "history", first_name = user_data.first_name,
                           email = user_data.email,
                           role = user_data.role,
                           user_status = user_data.user_status)


@staff_bp.route('/profile')
@login_required
@role_required('staff')
def profile():
    user_id = current_user.id
    user_data = User.query.filter_by(id = user_id).first()


    return render_template('staff/profile.html',
                           page = 'profile', first_name = user_data.first_name,
                           email = user_data.email,
                           role = user_data.role,
                           user_status = user_data.user_status)