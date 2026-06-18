from flask import Blueprint, render_template, redirect, url_for, flash, session
from forms.form import UserRegisterForm, StaffRegisterForm, LoginForm
from models import db
from models.model import User
from werkzeug.security import generate_password_hash
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
        form = UserRegisterForm()

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
            if role == 'user':
                approval_status = 'approved'
            else:
                approval_status = 'pending'
            new_user = User(first_name = first_name,
                            last_name = last_name,
                            email = email,
                            role = role,
                            user_status = approval_status)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            if role == 'user':
                flash(f'Account Created Successful for {first_name}', 'success')
            else:
                flash(f'Account Registration Successful for {first_name}', 'success')
                flash(f'You Can View Your Approval Status By Login with your Email And Password', 'info')
            return redirect(url_for('auth.login'))
    return render_template('auth/register.html', page = f'register {type}', form = form, type = type)


# @auth_bp.route('/register/staff', methods = ['GET', 'POST'])
# def registerStaff():

#     form = StaffRegisterForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(email = form.email.data).first()
#         if user:
#             flash('Staff With this email already exits', 'error')
#             return redirect(url_for('auth.login'))
        
#         else:
#             name = form.name.data
#             first_name = name.split()[0]
#             last_name = " ".join(name.split()[1:])
#             email = form.email.data
#             username = email.split("@")[0]
#             password = form.password.data
#             role = form.role.data

#             if role == 'staff':
#                 user_status = 'not_approved'
#             else:
#                 user_status = 'not_approved'

#             new_staff = User(first_name = first_name,
#                             last_name = last_name,
#                             email = email,
#                             username = username,
#                             role = role,
#                             user_status = user_status,
#                             password_hash = generate_password_hash(password))
#             db.session.add(new_staff)
#             db.session.commit()
#             flash(f'Account Created Successful for {first_name}', 'success')
#             flash(f'You Can View Your Approval Status By Login By your Email And Password', 'success')
#             return redirect(url_for('auth.login'))
#     return render_template('auth/register_staff.html', page = 'register', form = form)

@auth_bp.route("/logout")
@login_required
def logout():

    logout_user()
    session.clear()

    flash("Logged out successfully.")

    return redirect(url_for("auth.login"))