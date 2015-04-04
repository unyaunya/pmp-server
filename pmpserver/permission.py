#! python3
# -*- coding: utf-8 -*-

from collections import namedtuple
from functools import partial
from flask.ext.principal import Permission, RoleNeed, UserNeed

# Create a permission with a single Need, in this case a RoleNeed.
admin_permission = Permission(RoleNeed('admin'))


class ChangePasswordPermission(Permission):
    def __init__(self, userid):
        need = UserNeed(userid)
        super(ChangePasswordPermission, self).__init__(need)