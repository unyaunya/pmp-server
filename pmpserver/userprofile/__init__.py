#! python3
# -*- coding: utf-8 -*-

from flask import Blueprint

app = Blueprint(
    'userprofile',
    __name__,
    template_folder='templates',
    #static_folder='static'
)

from . import views