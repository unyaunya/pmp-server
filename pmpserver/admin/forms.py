#! python3
# -*- coding: utf-8 -*-

from ..forms import ModelForm
from ..models import User

class UserEditForm(ModelForm):
    class Meta:
        model = User
        exclude = ['password']

class UserEntryForm(ModelForm):
    class Meta:
        model = User
        include = ['id']
