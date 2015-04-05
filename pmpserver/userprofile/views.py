#! python3
# -*- coding: utf-8 -*-

from flask import request
from flask import render_template, flash, redirect, abort
from flask.ext.principal import Permission, UserNeed
from .. import db
from ..models import User
from .forms import ChangePasswordForm
from . import app

class ChangePasswordPermission(Permission):
    def __init__(self, userid):
        need = UserNeed(userid)
        super(ChangePasswordPermission, self).__init__(need)

@app.route('/change_password/<userid>', methods=['GET', 'POST'])
def change_password(userid):
    permission = ChangePasswordPermission(userid)
    if not permission.can():
        abort(403)  # HTTP Forbidden

    user = User.query.get_or_404(userid)
    form = ChangePasswordForm(request.form)
    if form.validate_on_submit():
        if user.password != form.old_password.data:
            flash("Invalid password.")
        else:
            user.password = form.new_password.data
            db.session.commit()
            flash("<%s>'s password was successfully changed." % user.id)
    return render_template('change_password.html', form=form, user=user)
