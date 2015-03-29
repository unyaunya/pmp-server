#! python3
# -*- coding: utf-8 -*-

from flask.ext.wtf import Form
from wtforms.fields import TextField, PasswordField, HiddenField
from wtforms import StringField, BooleanField
from wtforms.validators import Required, Email, DataRequired
from wtforms_alchemy import model_form_factory
from .models import User

BaseModelForm = model_form_factory(Form)

class ModelForm(BaseModelForm):
    @classmethod
    def get_session(self):
        return db.session

class LoginForm(Form):
    id = TextField('id', validators=[Required()])
    #email = TextField('ID', validators=[Email()])
    password = PasswordField('Password', validators=[Required('パスワードが入力されていません。')])
    remember_me = BooleanField('remember_me', default=False)

class ChangePasswordForm(Form):
    old_password = PasswordField('古いパスワード', validators=[Required('新しいパスワードが入力されていません。')])
    new_password = PasswordField('新しいワスワード', validators=[Required('古いパスワードが入力されていません。')])

class UserEditForm(ModelForm):
    class Meta:
        model = User
        exclude = ['password']

    #email = TextField('email', validators=[Email('メールアドレスの形式になっていません。')])
    #name = TextField('name', validators=[])
    #role = TextField('role', validators=[])

class UserEntryForm(ModelForm):
    class Meta:
        model = User
        include = ['id']
    #id = TextField('id', validators=[Required()])
    #password = PasswordField('Password', validators=[Required()])
