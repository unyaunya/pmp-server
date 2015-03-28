#! python3
# -*- coding: utf-8 -*-

import os
import json
import sqlite3
from contextlib import closing
from flask import Flask, Response, current_app, g, request, session, render_template, \
     flash, redirect, url_for
from datetime import datetime
from flask.ext.login import login_user, logout_user, current_user, login_required
from flask.ext.principal import Principal, UserNeed, RoleNeed
from flask.ext.principal import Identity, identity_loaded, identity_changed

from . import app, db, lm
from .forms import LoginForm, UserEntryForm, UserEditForm
from .models import User
from .permission import admin_permission


#from .util import ts

#-------------------------------------------------------------------------------
# for database
#-------------------------------------------------------------------------------


#-------------------------------------------------------------------------------
# for Login Manager / User Information Provider
#-------------------------------------------------------------------------------

@lm.user_loader
def load_user(id):
    return User.query.get(id)

lm.login_view = 'login'
lm.login_message = u"ようこそここへクッククック"

@app.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated():
        return redirect(url_for('index'))
    error = None
    form = LoginForm()
    if form.validate_on_submit():
        user = load_user(form.id.data)
        if (user is not None) and (form.password.data == user.passwd):
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


@identity_loaded.connect_via(app)
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

#-------------------------------------------------------------------------------
# for user management
#-------------------------------------------------------------------------------
@app.route('/users.html')
@admin_permission.require()
def users():
    return render_template('users.html', users=User.query.all())

@app.route('/edit_user/<userid>', methods=['GET', 'POST'])
def edit_user(userid):
    user = User.query.get_or_404(userid)
    form = UserEditForm()
    if form.validate_on_submit():
        form.copy_to(user)
        db.session.commit()
    form.copy_from(user)
    return render_template('edituser.html', form=form, user=user)

@app.route('/add_user', methods=['GET', 'POST'])
@admin_permission.require()
def add_user():
    form = UserEntryForm()
    if form.validate_on_submit():
        user = User()
        form.copy_to(user)
        db.session.add(user)
        db.session.commit()
        flash('New user was successfully posted')
        return redirect(url_for('add_user'))
    return render_template('adduser.html', form=form)


#-------------------------------------------------------------------------------
# protect a view with a principal for that need
@app.route('/admin')
@admin_permission.require()
def do_admin_index():
    return Response('Only if you are an admin')




#------------------------------------------------------------------------------

def projectsdir():
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), 'instance', 'projects')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/install.html')
def install():
    return render_template('install.html')

@app.route('/apikey.html')
def show_apikey():
    if 'logged_in' in session and session['logged_in'] == True:
        return render_template('apikey.html')
    else:
        return redirect(url_for('login'))
        #return render_template('login.html', error='APIキーを表示するにはログインしてください')

@app.route('/project_list.html')
def project_list():
    path = projectsdir()
    files = [x for x in os.listdir(path) if os.path.isdir(os.path.join(path, x))]
    return render_template('projects.html', projects=files)

@app.route('/delete_user/<userid>', methods=['POST'])
def delete_user(userid):
    return redirect(url_for('users'))

#handle http request(Web API)
@app.route('/pmp/api/projects/')
def api_project_list():
    return json.dumps(os.listdir(projectsdir()), ensure_ascii=False)

@app.route('/pmp/api/projects/<projectname>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def api_projects(projectname):
    def _get_project(projectname):
        path = os.path.join(projectsdir(), projectname, 'current.json.txt')
        if not os.path.exists(path):
            return ('Not Found %s' % path, 404, [])
        return open(path, encoding='utf-8').read()
    #-------
    print('projectname=[%s]' % projectname)
    if request.method == 'GET':
        return _get_project(projectname)
    elif request.method == 'POST':
        #f = request.files['the_file']
        #f.save('/var/www/uploads/uploaded_file.txt')
        #print(request.args)
        #print(request.form)
        print(request.remote_addr, request.remote_user)
        _now = datetime.now()
        path = os.path.join(projectsdir(), projectname, 'old',
            '%s_%s.txt' % (_now.strftime("%Y%m%d%H%M%S"), request.remote_addr))
        print(path)
        with open(path, "w", encoding='utf-8') as f:
            f.write(request.form['data'])
        return 'OK'
    else:
        path = os.path.join(projectsdir(), projectname, 'current.json.txt')
        if not os.path.exists(path):
            return ('Not Found %s' % path, 404, [])
        return open(path, encoding='utf-8').read()
