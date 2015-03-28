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

OPENID_PROVIDERS = [
    {'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id'},
    {'name': 'Yahoo', 'url': 'https://me.yahoo.com'},
    {'name': 'AOL', 'url': 'http://openid.aol.com/<username>'},
    {'name': 'Flickr', 'url': 'http://www.flickr.com/<username>'},
    {'name': 'MyOpenID', 'url': 'https://www.myopenid.com'}]