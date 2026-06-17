from flask import Blueprint, render_template, redirect, url_for, flash, session
from flask_login import logout_user

error_bp = Blueprint('error', __name__)

@error_bp.app_errorhandler(404)
def page_not_found(error):
    return render_template('error/404.html'), 404


@error_bp.app_errorhandler(500)
def server_not_found(error):
    return render_template('error/500.html'), 500

@error_bp.app_errorhandler(403)
def forbidden(error):

    logout_user()
    session.clear()
    flash(
        "Your session was terminated because you tried to access an unauthorized page.",
        "danger"
    )
    return render_template('error/403.html'), 403