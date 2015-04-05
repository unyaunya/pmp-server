#! python3
# -*- coding: utf-8 -*-

from flask import current_app, request
from flask import render_template, flash, redirect, url_for
from flask.ext.login import login_user, logout_user, current_user, login_required
from flask.ext.principal import Identity, identity_loaded, identity_changed
from flask.ext.principal import RoleNeed, UserNeed

from .. import app as App
from .. import lm
from ..models import User
from .forms import LoginForm

from . import app

#-------------------------------------------------------------------------------
# for Login Manager / User Information Provider
#-------------------------------------------------------------------------------

@lm.user_loader
def load_user(id):
    return User.query.get(id)

lm.login_view = 'login.login'
lm.login_message = u"ようこそここへクッククック"

@app.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated():
        return redirect(url_for('index'))
    error = None
    form = LoginForm()
    if form.validate_on_submit():
        user = load_user(form.id.data)
        if (user is not None) and (form.password.data == user.password):
            login_user(user, remember=form.remember_me.data)
            # Tell Flask-Principal the identity changed
            identity_changed.send(current_app._get_current_object(),
                                  identity=Identity(user.id))
            flash('You were logged in')
            return redirect(request.args.get('next') or url_for('index'))
        error = 'Invalid id or password'
    return render_template('login.html', form=form, error=error)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You were logged out')
    return redirect(url_for('index'))

#-------------------------------------------------------------------------------
# for User Information
#-------------------------------------------------------------------------------
@identity_loaded.connect_via(App)
def on_identity_loaded(sender, identity):
    # Set the identity user object
    identity.user = current_user

    # Add the UserNeed to the identity
    if hasattr(current_user, 'id'):
        identity.provides.add(UserNeed(current_user.id))

    # Assuming the User model has a list of roles, update the
    # identity with the roles that the user provides
    if hasattr(current_user, 'roles'):
        for role in current_user.roles:
            identity.provides.add(RoleNeed(role.name))
    if hasattr(current_user, 'role'):
        identity.provides.add(RoleNeed(current_user.role))
