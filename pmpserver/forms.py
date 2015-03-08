#! python3
# -*- coding: utf-8 -*-

from flask.ext.wtf import Form
from wtforms.fields import TextField, PasswordField
from wtforms.validators import Required, Email

class EmailPasswordForm(Form):
    #email = TextField('Email', validators=[Required(), Email()])
    email = TextField('Email', validators=[Required()])
    password = PasswordField('Password', validators=[Required()])