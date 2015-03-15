#! python3
# -*- coding: utf-8 -*-

import os
basedir = os.path.abspath(os.path.dirname(__file__))

BASEDIR = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = "postgresql://user:password@localhost/spaceshipDB"
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
DATABASE = 'pmp.db'
USERID   = 'admin'
PASSWORD = 'default'

WTF_CSRF_ENABLED = True
SECRET_KEY = 'development key'
