from app import app
from models import db
from models.model import User, AdminProfile


with app.app_context():
    # Create all database tables
    db.create_all()

    # Create default admin if it doesn't exist
    if not User.query.filter_by(role="admin").first():
        admin = User(
            email="admin@test.com",
            password="admin",
            role="admin",
            is_approved=True,
            is_active=True,
            first_name="Admin"
        )

        admin.admin_profile = AdminProfile()

        db.session.add(admin)
        db.session.commit()

        print("Admin user created successfully.")
    else:
        print("Admin user already exists.")

    print("Database setup completed successfully.")