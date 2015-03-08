#! python3
# -*- coding: utf-8 -*-

import os
import json
import sqlite3
from contextlib import closing
from flask import Flask, g, request, session, render_template, \
     flash, redirect, url_for
from datetime import datetime

from . import app
from .forms import EmailPasswordForm
#from .util import ts

def init_db():
    """DB初期化。コマンドラインから呼び出す"""
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql') as f:
            db.cursor().executescript(f.read().decode('utf-8'))
        db.commit()

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def get_user(userid):
    cur = g.db.execute('select id, passwd, email, name, apikey, role from users where id = ?', [userid])
    users = [dict(id=row[0], passwd=row[1], email=row[2], name=row[3],
                apikey=row[4], role=row[5]) for row in cur.fetchall()]
    if len(users) != 1:
        return None
    else:
        return users[0]

def projectsdir():
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), 'instance', 'projects')

@app.before_request
def before_request():
    g.db = connect_db()
    #g.user = get_user

@app.teardown_request
def teardown_request(exception):
    g.db.close()

@app.route('/login', methods=["GET", "POST"])
def login():
    error = None
    form = EmailPasswordForm()
    if form.validate_on_submit():
        print('validated')
        # パスワードのチェックとログイン処理
        # [...]
        print(form.email)
        print(form.email.data)
        print(form.password)
        print(form.password.data)
        return redirect(url_for('index'))
        if form.email.data != app.config['USERID']:
            error = 'Invalid userid'
        elif form.password.data != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            session['userid'] = form.email.data
            flash('You were logged in')
            return redirect(url_for('index'))
    return render_template('login.html', form=form, error=error)

@app.route('/login', methods=['GET', 'POST'])
def __login():
    error = None
    if request.method == 'POST':
        if request.form['userid'] != app.config['USERID']:
            error = 'Invalid userid'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            session['userid'] = request.form['userid']
            flash('You were logged in')
            return redirect(url_for('index'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('index'))

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

@app.route('/users.html')
def users():
    cur = g.db.execute('select id, passwd, email, name, apikey from users order by id desc')
    users = [dict(id=row[0], passwd=row[1], email=row[2], name=row[3],
               apikey=row[4]) for row in cur.fetchall()]
    return render_template('users.html', users=users)

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'GET':
        return render_template('adduser.html')
    elif request.method == 'POST':
        if not session.get('logged_in'):
            abort(401)
        #print(request.form)
        data = [request.form['id'],
                request.form['passwd'],
                request.form['email'],
                request.form['name'],
                'admin' if 'admin' in request.form else '']
        #print(data)
        g.db.execute("insert into users (id, passwd, email, name, apikey, role) values (?, ?, ?, ?, '', ?)", data)
        g.db.commit()
        flash('New user was successfully posted')
        return redirect(url_for('add_user'))

@app.route('/edit_user/<userid>', methods=['GET', 'POST'])
def edit_user(userid):
    if request.method == 'GET':
        user = get_user(userid)
        if user['role'] == 'admin':
            user['admin'] = 'checked'
        if user is not None:
            return render_template('edituser.html', user=user)
    elif request.method == 'POST':
        return render_template('edituser.html')

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
