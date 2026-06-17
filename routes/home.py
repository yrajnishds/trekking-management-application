from flask import Blueprint, render_template, redirect, url_for, flash, session
from flask_login import current_user, logout_user

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def index():
    return redirect(url_for('home.home'))


@home_bp.route('/home')
def home():
    if current_user.is_authenticated:
        logout_user()
        session.clear()
        flash(
        "Your session was terminated because you access an Home page.",
        "danger")
    return render_template('home.html', page = "Home")