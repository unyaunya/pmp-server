#! python3
# -*- coding: utf-8 -*-

import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.principal import Principal, Permission, RoleNeed

#create flask application
app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)

principals = Principal(app)

from pmpserver import views, models

from . import admin
app.register_blueprint(admin.app, url_prefix="/admin")

from . import userprofile
app.register_blueprint(userprofile.app, url_prefix="/userprofile")