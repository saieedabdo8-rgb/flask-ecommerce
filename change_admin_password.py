import os
from app import app, db, Admin

with app.app_context():
admin = Admin.query.filter_by(username='admin').first()
if not admin:
    admin = Admin.query.filter_by(username='abdosaieed').first()
if not admin:
    admin = Admin.query.filter_by(username='Abdelrhman').first()

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
