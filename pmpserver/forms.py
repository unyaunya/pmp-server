#! python3
# -*- coding: utf-8 -*-

from flask.ext.wtf import Form
from wtforms.fields import TextField, PasswordField, HiddenField
from wtforms import StringField, BooleanField
from wtforms.validators import Required, Email, DataRequired

class LoginForm(Form):
    id = TextField('id', validators=[Required()])
    #email = TextField('ID', validators=[Email()])
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('remember_me', default=False)

class UserEditForm(Form):
    email = TextField('email', validators=[Email()])
    name = TextField('name', validators=[])
    role = TextField('role', validators=[])

    def copy_to(self, user):
        user.email = self.email.data
        user.name = self.name.data
        user.role = self.role.data

    def copy_from(self, user):
        self.email.data = user.email
        self.name.data = user.name
        self.role.data = user.role

class UserEntryForm(UserEditForm):
    id = TextField('id', validators=[Required()])
    password = PasswordField('Password', validators=[Required()])

    def copy_to(self, user):
        super(UserEntryForm, self).copy_to(user)
        user.id = self.id.data
        user.passwd = self.password.data

    def copy_from(self, user):
        super(UserEntryForm, self).copy_from(user)
        self.id.data = user.id
        self.password.data = user.passwd
