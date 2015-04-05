#! python3
# -*- coding: utf-8 -*-

from flask.ext.wtf import Form
from wtforms.fields import TextField, PasswordField
from wtforms import BooleanField
from wtforms.validators import Required, Email, DataRequired
from wtforms_alchemy import model_form_factory

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
