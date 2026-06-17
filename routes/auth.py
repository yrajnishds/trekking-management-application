from flask import Blueprint, render_template, redirect, url_for, flash
from forms.form import UserRegisterForm, StaffRegisterForm, LoginForm
from models import db
from models.model import User
from werkzeug.security import generate_password_hash


auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/', methods = ['GET', 'POST'])
@auth_bp.route('/login', methods = ['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        # Checking User
        if user and user.check_password(form.password.data):
            role = user.role
            return redirect(url_for(f'{role}.dashboard'))
        else:
            flash('Invalid email or password', 'error')
            return redirect(url_for('auth.login'))
    return render_template('auth/login.html', page = 'Login', form = form)



@auth_bp.route('/register/user', methods = ['GET', 'POST'])
def registerUser():

    form = UserRegisterForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user:
            flash('User this email already exits', 'error')
            return redirect(url_for('auth.login'))
        
        else:
            name = form.name.data
            first_name = name.split()[0]
            last_name = " ".join(name.split()[1:])
            email = form.email.data
            username = email.split("@")[0]
            password = form.password.data
            role = form.role.data

            if role == 'user':
                user_status = 'approved'
            else:
                user_status = 'not_approved'

            new_user = User(first_name = first_name,
                            last_name = last_name,
                            email = email,
                            username = username,
                            role = role,
                            user_status = user_status,
                            password_hash = generate_password_hash(password))
            db.session.add(new_user)
            db.session.commit()
            flash(f'Account Created Successful for {first_name}', 'success')
            return redirect(url_for('auth.login'))
    return render_template('auth/register_user.html', page = 'register', form = form)


@auth_bp.route('/register/staff', methods = ['GET', 'POST'])
def registerStaff():

    form = StaffRegisterForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user:
            flash('Staff With this email already exits', 'error')
            return redirect(url_for('auth.login'))
        
        else:
            name = form.name.data
            first_name = name.split()[0]
            last_name = " ".join(name.split()[1:])
            email = form.email.data
            username = email.split("@")[0]
            password = form.password.data
            role = form.role.data

            if role == 'staff':
                user_status = 'not_approved'
            else:
                user_status = 'not_approved'

            new_staff = User(first_name = first_name,
                            last_name = last_name,
                            email = email,
                            username = username,
                            role = role,
                            user_status = user_status,
                            password_hash = generate_password_hash(password))
            db.session.add(new_staff)
            db.session.commit()
            flash(f'Account Created Successful for {first_name}', 'success')
            flash(f'You Can View Your Approval Status By Login By your Email And Password', 'success')
            return redirect(url_for('auth.login'))
    return render_template('auth/register_staff.html', page = 'register', form = form)

auth_bp.route('/logout')
def logout():
    return redirect(url_for('home.home'))