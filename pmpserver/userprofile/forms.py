#! python3
# -*- coding: utf-8 -*-

from flask.ext.wtf import Form
from wtforms.validators import Required
from wtforms.fields import PasswordField

class ChangePasswordForm(Form):
    old_password = PasswordField('古いパスワード', validators=[Required('新しいパスワードが入力されていません。')])
    new_password = PasswordField('新しいワスワード', validators=[Required('古いパスワードが入力されていません。')])
