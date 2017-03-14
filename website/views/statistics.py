from flask import (Blueprint, render_template, request,
                   flash, redirect, url_for, session)

from werkzeug.utils import secure_filename

import os
import time
import csv
import io

from website import app
from website.views.account import login_required
from website.models.user import User


statistics = Blueprint('statistics',
                       __name__,
                       template_folder='../templates/statistics',
                       url_prefix='/statistics')

@statistics.route('/', methods=['GET', 'POST'])
def index():
    user = User.get_user_by_user_id(session.get('userid'))
    if request.method == 'GET':
        return render_template('index.html', user=user)
    serial_id = request.form['serial_id']
    # TODO: get sheet by serial id.
    return render_template('show_table_detail.html',
                           user=user,
                           serial_id=serial_id)


@statistics.route('/publish_table/', methods=['GET', 'POST'])
@login_required
def publish_table():
    if request.method == 'GET':
        return render_template('publish_table.html')

    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)

    # if user does not select file, browser also
    # submit a empty part without filename
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    # get csv file
    if file and _allowed_file(file.filename):
        utf8_converted_str = file.stream.read().decode('utf-8')
        csvdict = csv.reader(io.StringIO(utf8_converted_str))
        example = []
        for line in csvdict:
            example.append(line)
        table_head = example[0]
        table_rows = example[1:]
        return render_template('publish_table.html',
                               table_head=table_head,
                               table_rows=table_rows)

@statistics.route('/save_example_table/', methods=['GET', 'POST'])
@login_required
def save_example_table ():
    if request.method == 'POST':
        table_head = request.form['table_head']
        table_rows = request.form['table_rows']
        print(table_head)
        print(table_rows)
        return render_template('save_example_table.html')


def _allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']
