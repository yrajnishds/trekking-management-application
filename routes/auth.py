from flask import Blueprint, render_template, redirect, url_for, flash, session
from forms.form import TrekkerRegisterForm, StaffRegisterForm, LoginForm
from models import db
from models.model import User
from flask_login import login_user, login_required, logout_user


auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods = ['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        # Checking User
        if user and user.check_password(form.password.data):
            role = user.role

            login_user(user)

            return redirect(url_for(f'{role}.dashboard'))
        else:
            flash('Invalid email or password', 'error')
            return redirect(url_for('auth.login'))
    return render_template('auth/login.html', page = 'Login', form = form)



@auth_bp.route('/register/<string:type>', methods = ['GET', 'POST'])
def register(type):
    if type == 'staff':
        form = StaffRegisterForm()
    else:
        form = TrekkerRegisterForm()

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
            if role == 'trekker':
                flash(f'Account Created Successful for {first_name}', 'success')
            else:
                flash(f'Account Registration Successful for {first_name}', 'success')
                flash(f'You Can View Your Approval Status By Login with your Email And Password', 'info')
            return redirect(url_for('auth.login'))
    return render_template('auth/register.html', page = f'register {type}', form = form, type = type)


@auth_bp.route("/logout")
@login_required
def logout():

    logout_user()
    session.clear()

    flash("Logged out successfully.")

    return redirect(url_for("auth.login"))