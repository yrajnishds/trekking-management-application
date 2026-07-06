from flask import Flask
from flask_login import LoginManager
from models.model import User

from routes.home import home_bp
from routes.auth import auth_bp
from routes.admin import admin_bp
from routes.trekker import trekker_bp
from routes.staff import staff_bp
from routes.error import error_bp

from models import db


def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = 'mad1-project'
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.sqlite3"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    with app.app_context():  # Create the Database
        db.create_all()

        print('Database Created Successfuly')

        from create_admin import create_admin_user
        create_admin_user()
    
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please Login First'
    @login_manager.user_loader

    def load_user(user_id):

        return db.session.get(User, int(user_id))
    



    app.register_blueprint(home_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(trekker_bp)
    app.register_blueprint(staff_bp)
    app.register_blueprint(error_bp)

    return app

app = create_app()
if __name__ == "__main__":
    app.run(debug=True, port=5001)