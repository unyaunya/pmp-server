#! python3
# -*- coding: utf-8 -*-

from . import db
from sqlalchemy_utils import PasswordType

class User(db.Model):
    # Columns
    id = db.Column(db.String, primary_key=True)
    password = db.Column(
        PasswordType(
            schemes=['pbkdf2_sha512']
        ),
        nullable=False
    )

    email = db.Column(db.String)
    name = db.Column(db.String)
    role = db.Column(db.String)
    apikey = db.Column(db.String)
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def __repr__(self):
        return '<User %r email=%s>' % (self.id, self.email)


class DataDictionary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    definition = db.Column(db.String)

    def __repr__(self):
        return '<Data %s = %s>' % (self.id, self.definition)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post %r>' % (self.body)