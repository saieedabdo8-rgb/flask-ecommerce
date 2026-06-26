import os
from app import app, db, Admin

with app.app_context():
    admin = Admin.query.filter_by(username='admin').first()
    if admin:
        admin.set_password('saieedabdo')
        db.session.commit()
        print('✅ Password changed to: saieedabdo')
    else:
        print('Admin not found. Creating new admin...')
        admin = Admin(username='admin')
        admin.set_password('saieedabdo')
        db.session.add(admin)
        db.session.commit()
        print('✅ Admin created with password: saieedabdo')
