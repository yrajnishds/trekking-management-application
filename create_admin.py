from models import db
from models.model import User


def create_admin_user():
    # Check if admin exists, if not create
    if not User.query.filter_by(role='admin').first():
        admin = User(username='admin', email='admin@example.com',
                     role='admin', user_status = 'approved',
                     first_name = 'Admin')
        admin.set_password('admin')
        db.session.add(admin)
        db.session.commit()
        print("Admin user created.")
    else:
        print("Admin user already exists.")
