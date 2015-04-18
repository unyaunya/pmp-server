#! python3
# -*- coding: utf-8 -*-

from flask import request
from flask import render_template, flash, redirect, abort, url_for
from flask.ext.principal import Permission, UserNeed
from .. import db
from ..models import DataDictionary
from .forms import DataDictionaryEditForm, DataDictionaryEntryForm
from . import app

@app.route('/entries.html')
def entries():
    return render_template('/entries.html', entries=DataDictionary.query.all())

@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    entry = DataDictionary.query.get_or_404(id)
    form = DataDictionaryEditForm(request.form, entry)
    if form.validate_on_submit():
        form.populate_obj(entry)
        db.session.commit()
    return render_template('edit.html', form=form, entry=entry)

@app.route('/add', methods=['GET', 'POST'])
def add():
    form = DataDictionaryEntryForm(request.form)
    if form.validate_on_submit():
        entry = DataDictionary()
        form.populate_obj(entry)
        db.session.add(entry)
        db.session.commit()
        flash('New entry was successfully posted')
        return redirect(url_for('.add'))
    return render_template('add.html', form=form)

@app.route('/delete/<id>')
def delete(id):
    entry = DataDictionary.query.get_or_404(id)
    db.session.delete(entry)
    db.session.commit()
    return redirect(url_for('.entries'))

