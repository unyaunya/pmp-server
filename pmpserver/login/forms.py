#! python3
# -*- coding: utf-8 -*-

from flask.ext.wtf import Form
from wtforms.fields import TextField, PasswordField
from wtforms import BooleanField
from wtforms.validators import Required

class LoginForm(Form):
    id = TextField('id', validators=[Required()])
    password = PasswordField('Password', validators=[Required('パスワードが入力されていません。')])
    remember_me = BooleanField('remember_me', default=False)
