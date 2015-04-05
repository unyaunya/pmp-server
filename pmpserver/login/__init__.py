#! python3
# -*- coding: utf-8 -*-

from flask import Blueprint

app = Blueprint(
    'login',
    __name__,
    template_folder='templates'
)

from . import views