#! python3
# -*- coding: utf-8 -*-

from . import db

class User(db.Model):
    # Columns
    id = db.Column(db.String, primary_key=True)
    passwd = db.Column(db.String)
    email = db.Column(db.String)
    name = db.Column(db.String)
    role = db.Column(db.String)
    apikey = db.Column(db.String)
