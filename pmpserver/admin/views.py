#! python3
# -*- coding: utf-8 -*-

#from flask import Flask, Response, current_app, g, request, session
from flask import request
from flask import render_template, flash, redirect, url_for
from flask.ext.principal import Permission, RoleNeed
from .. import db
from ..models import User
from .forms import UserEntryForm, UserEditForm
from . import app

#-------------------------------------------------------------------------------
# Permission
#-------------------------------------------------------------------------------
# Create a permission with a single Need, in this case a RoleNeed.
admin_permission = Permission(RoleNeed('admin'))

#-------------------------------------------------------------------------------
# for user management
#-------------------------------------------------------------------------------
@app.route('/users.html')
@admin_permission.require()
def users():
    return render_template('/users.html', users=User.query.all())

@app.route('/edit_user/<userid>', methods=['GET', 'POST'])
def edit_user(userid):
    user = User.query.get_or_404(userid)
    form = UserEditForm(request.form, user)
    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.commit()
    return render_template('edituser.html', form=form, user=user)

@app.route('/add_user', methods=['GET', 'POST'])
@admin_permission.require()
def add_user():
    form = UserEntryForm(request.form)
    if form.validate_on_submit():
        user = User()
        form.populate_obj(user)
        db.session.add(user)
        db.session.commit()
        flash('New user was successfully posted')
        return redirect(url_for('.add_user'))
    return render_template('adduser.html', form=form)

@app.route('/delete_user/<userid>')
@admin_permission.require()
def delete_user(userid):
    user = User.query.get_or_404(userid)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('.users'))

@app.route('/password_reset/<userid>')
@admin_permission.require()
def password_reset(userid):
    user = User.query.get_or_404(userid)
    user.password = user.id
    db.session.commit()
    flash("<%s>'s password was successfully reset to the same as the user id." % user.id)
    return redirect(url_for('.users'))
