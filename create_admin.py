from models import db
from models.model import User
from werkzeug.security import generate_password_hash

admin = User.query.filter_by(email = 'admin@test.com').first()

if not admin:

    admin = User(first_name = 'Admin', 
                    email = 'admin@test.com', username='admin',
                    password_hash = generate_password_hash('admin'),
                    role = 'admin', user_status = 'approved')
    db.session.add(admin)
    db.session.commit()