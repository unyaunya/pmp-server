#! python3
# -*- coding: utf-8 -*-

#from flask.ext.wtf import Form
#from wtforms.validators import Required

from ..forms import ModelForm
from ..models import DataDictionary

class DataDictionaryEditForm(ModelForm):
    class Meta:
        model = DataDictionary
        include = ['name']

class DataDictionaryEntryForm(ModelForm):
    class Meta:
        model = DataDictionary
        include = ['name']

