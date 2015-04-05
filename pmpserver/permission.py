#! python3
# -*- coding: utf-8 -*-

from collections import namedtuple
from functools import partial
from flask.ext.principal import Permission, RoleNeed, UserNeed

class ChangePasswordPermission(Permission):
    def __init__(self, userid):
        need = UserNeed(userid)
        super(ChangePasswordPermission, self).__init__(need)