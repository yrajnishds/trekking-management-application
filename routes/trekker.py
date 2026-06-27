from flask import Blueprint, render_template, redirect, url_for
from flask import request, session, flash
from flask_login import current_user, login_required
from models import db
from models.model import User, Trek, Booking
from routes.decorators import role_required
from forms.trek_form import TrekBookForm



trekker_bp = Blueprint('trekker', __name__)


@trekker_bp.route('/dashboard')
@login_required
@role_required('trekker')
def dashboard():
    trekker_id = current_user.id
    trekker_data = User.query.filter_by(id = trekker_id).first()
    return render_template('trekker/dashboard.html',
                           page = 'dashboard', first_name = trekker_data.first_name,
                           email = trekker_data.email,
                           role = trekker_data.role)


@trekker_bp.route('/trek')
@login_required
@role_required('trekker')
def trek():
    trekker_id = current_user.id
    trekker_data = User.query.filter_by(id = trekker_id).first()
    treks = Trek.query.all()
    return render_template('trekker/trek.html',
                           page = 'Treks', first_name = trekker_data.first_name,
                           email = trekker_data.email,
                           role = trekker_data.role,
                           treks = treks)

@trekker_bp.route('/booking')
@login_required
@role_required('trekker')
def booking():
    form = TrekBookForm()
    bookings = Booking.query.filter_by(trekker_id = current_user.id).all()
    treks = Trek.query.filter_by(
        trek_status = 'open').filter(Trek.booked_slots < Trek.slots)
    form.trekker_id.choices = [(current_user.id, current_user.first_name)]
    # form.trek_id.choices = ['', '--- Select Trek ---'] + [(trek.id, trek.trek_code) for trek in available_treks]
    form.trek_id.choices = [('', '---Choose Treks---')] + [(trek.id, trek.trek_code) for trek in treks]
    trek = Trek.query.all()
    return render_template('trekker/booking.html',
                           page = 'booking',
                           trek = trek,
                           form = form,
                           bookings = bookings
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
    trekker_id = current_user.id
    trekker_data = User.query.filter_by(id = trekker_id).first()


    return render_template('trekker/profile.html',
                           page = 'profile', first_name = trekker_data.first_name,
                           email = trekker_data.email,
                           role = trekker_data.role)
