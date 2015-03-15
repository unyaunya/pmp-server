#! python3
# -*- coding: utf-8 -*-

import os

basedir = os.path.abspath(os.path.dirname(__file__))
#configuration

BASEDIR = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "pmp.db")
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

USERID   = 'root'
PASSWORD = 'default'
SECRET_KEY = 'development key'
