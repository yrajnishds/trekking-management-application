from models import db
from models.model import User, AdminProfile


def create_admin_user():
    # Check if admin exists, if not create
    if not User.query.filter_by(role='admin').first():
        admin = User(email='admin@test.com',
                     password = 'admin',
                     role='admin', is_approved = True,
                     is_active = True,
                     first_name = 'admin')
        admin.admin_profile = AdminProfile()
        db.session.add(admin)
        db.session.commit()
        print("Admin user created.")
    else:
        print("Admin user already exists.")
