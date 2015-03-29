#!flask/bin/python
from pmpserver import db
from pmpserver.models import User

def add_admin():
    admin = User()
    admin.id = 'admin'
    admin.password = 'admin'
    admin.name = 'admin'
    admin.email = 'foo@bar.com'
    admin.role = 'admin'
    db.session.add(admin)
    db.session.commit()

if __name__ == '__main__':
    add_admin()
