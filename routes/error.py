from flask import Blueprint, render_template, redirect, url_for, flash, session
from flask_login import logout_user, current_user

error_bp = Blueprint('error', __name__)

@error_bp.app_errorhandler(404)
def page_not_found(error):
    return render_template('error/404.html', page = '404 - error'), 404


@error_bp.app_errorhandler(500)
def page_not_found(error):
    return render_template('error/500.html', page = '500 - error'), 500



@error_bp.app_errorhandler(403)
def forbidden(error):

    return render_template('error/403.html', page = '403 - Error'), 403