from flask import Blueprint, render_template, redirect, url_for, flash, session
from forms.user_form import TrekkerRegisterForm, StaffRegisterForm, LoginForm
from models import db
from models.model import User, TrekkerProfile, StaffProfile
from flask_login import login_user, login_required
from flask_login import current_user, logout_user


auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods = ['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        # Checking User
        if user and user.password == form.password.data:
            if user.is_blocked:
                flash('You  Account is blocked Please Contact admin', 'info')
                return redirect(url_for('auth.login'))
            
            if not user.is_active:
                flash('You  Account is Deactivated Please Try again after some time', 'info')
                return redirect(url_for('auth.login'))
            
            if not user.is_approved:
                flash('You  Account is Status id pending Please Try after sum time....', 'info')
                return redirect(url_for('auth.login'))

            login_user(user)
            role = current_user.role

            return redirect(url_for(f'{role}.dashboard'))
        else:
            flash('Invalid email or password', 'warning')
            return redirect(url_for('auth.login'))
    return render_template('auth/login.html', page = 'Login', form = form)



@auth_bp.route('/register/<string:role_type>', methods = ['GET', 'POST'])
def register(role_type):
    if role_type == 'staff':
        form = StaffRegisterForm()
    else:
        form = TrekkerRegisterForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user:
            flash(f'{user.role.caplitalize()} With this email already exits', 'warning')
            return redirect(url_for('auth.register'))
        
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
                return redirect(url_for('auth.login'))
            else:
                flash(f'Account Registration Successful for {first_name}', 'success')
                flash(f'You Can View Your Approval Status By Login with your Email And Password', 'info')
                return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', page = f'register {role_type}', form = form, role_type = role_type)


@auth_bp.route("/logout")
@login_required
def logout():

    logout_user()
    session.clear()

    flash("Logged out successfully.", 'info')

    return redirect(url_for("auth.login"))