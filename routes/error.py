from flask import Blueprint, render_template

error_bp = Blueprint('error', __name__)

error_bp.app_errorhandler(404)
def page_not_found(error):
    return render_template('error/500.html'), 404


error_bp.app_errorhandler(500)
def server_not_found(error):
    return render_template('error/500.html'), 500
