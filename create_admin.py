from models import db
from models.model import User


def create_admin_user():
    # Check if admin exists, if not create
    if not User.query.filter_by(role='admin').first():
        admin = User(username='admin', email='admin@test.com',
                     role='admin', approval_status = 'approved',
                     is_active = True,
                     first_name = 'admin')
        admin.set_password('admin')
        db.session.add(admin)
        db.session.commit()
        print("Admin user created.")
    else:
        print("Admin user already exists.")
