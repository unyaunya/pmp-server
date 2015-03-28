#! python3
# -*- coding: utf-8 -*-

from flask.ext.principal import Permission, RoleNeed

# Create a permission with a single Need, in this case a RoleNeed.
admin_permission = Permission(RoleNeed('admin'))
