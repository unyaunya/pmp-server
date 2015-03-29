#! python3
# -*- coding: utf-8 -*-

import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = "postgresql://user:password@localhost/spaceshipDB"
SQLALCHEMY_MIGRATE_REPO = os.path.join(BASEDIR, 'db_repository')

SECRET_KEY = 'development key'
