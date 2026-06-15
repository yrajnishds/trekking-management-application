from flask import Blueprint, render_template

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/')
@auth_bp.route('/login')
def login():
    return render_template('auth/login.html', page = 'Login')



@auth_bp.route('/register')
def register():
    return render_template('auth/register.html', page = 'register')



@auth_bp.route('/logout')
def logout():
    return render_template('home.html', page = 'home')