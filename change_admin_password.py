import os
from app import app, db, Admin

with app.app_context():
    admin = Admin.query.first()
    if admin:
        admin.username = 'Abdelrhman'
        admin.set_password('saieedabdo')
        db.session.commit()
        print('✅ Updated: Abdelrhman / saieedabdo')
    else:
        admin = Admin(username='Abdelrhman')
        admin.set_password('saieedabdo')
        db.session.add(admin)
        db.session.commit()
        print('✅ Created: Abdelrhman / saieedabdo')
