from dateutil import parser
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import Note
import json
import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
from . import db

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')
        if len(note) < 1:
            flash('Note is too short', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note Added successfully', category='success')
            return redirect(url_for('views.home'))
    return render_template("home.html", user=current_user, notes=Note.query.all())


@views.route('/waifu')
@login_required
def waifu():
    r = requests.get('https://api.waifu.im/random/')
    response = r.text
    link = json.loads(response)
    link = link['images'][0]['preview_url']
    link = link.split('=')
    l = link[1]
    link = 'https://cdn.waifu.im/'+l
    return render_template('anime.html',url=link, user=current_user)
    # return link

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})


@views.app_template_filter('strftime')
def _jinja2_filter_datetime(date, fmt=None):
    date = parser.parse(date)
    native = date.replace(tzinfo=None)
    format = '%m/%d/%Y, %H:%M:%S'
    return native.strftime(format)
