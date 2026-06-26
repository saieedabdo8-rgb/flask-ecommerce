import os
from app import app, db, Admin

with app.app_context():
    admin = Admin.query.filter_by(username='admin').first()
    if not admin:
        admin = Admin.query.filter_by(username='abdosaieed').first()

    if admin:
        admin.username = 'abdosaieed'
        admin.set_password('saieedabdo')
        db.session.commit()
        print('✅ Updated: abdosaieed / saieedabdo')
    else:
        admin = Admin(username='abdosaieed')
        admin.set_password('saieedabdo')
        db.session.add(admin)
        db.session.commit()
        print('✅ Created: abdosaieed / saieedabdo')
