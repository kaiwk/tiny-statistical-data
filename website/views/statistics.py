from flask import (Blueprint, render_template, request,
                   flash, redirect, url_for, session, g)

from werkzeug.utils import secure_filename

import csv
import io

from website import app
from website.views.account import login_required
from website.models.user import User
from website.models.statistical_table import StatisticalTable
from website.models.statistical_table_item import StatisticalTableItem


statistics = Blueprint('statistics',
                       __name__,
                       template_folder='../templates/statistics',
                       url_prefix='/statistics')

@statistics.route('/', methods=['GET', 'POST'])
def index():
    user = User.get_user_by_user_id(session.get('userid'))
    if request.method == 'GET':
        return render_template('index.html', user=user)



@statistics.route('/fill_in_table/', methods=['GET', 'POST'])
def fill_in_table():

    if request.method == 'GET':
        serial_key = request.args.get('serial_key', '')

        statistical_table = StatisticalTable.get_statistical_table_by_serial_key(serial_key)
        tablename = statistical_table.name
        g.statistical_table_id = statistical_table.tableid

        # get head and sample rows
        head = statistical_table.head
        sample = statistical_table.sample
        csv_str = '\n'.join((head, sample))
        csvlist = csv.reader(io.StringIO(csv_str))
        temp = [line for line in csvlist]
        head = temp[0]
        rows = temp[1:]

        return render_template('fill_in_table.html',
                               tablename=tablename,
                               head=head,
                               rows=rows,
                               serial_key=serial_key)

    # save table item
    if request.method == 'POST':
        temp = [k.strip() + ':' + v.strip() for k, v in request.form.items()]
        content = ','.join(temp)
        tableid = request.form['tableid']

        current_count = StatisticalTableItem.get_count()
        order_num = current_count + 1
        # StatisticalTableItem.save(order_num, content, tableid)
        return "Success"




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
        csvlist = csv.reader(io.StringIO(utf8_converted_str))
        temp = [line for line in csvlist]
        table_head = temp[0]
        table_rows = temp[1:]
        g.table_example = utf8_converted_str
        return render_template('publish_table.html',
                               table_head=table_head,
                               table_rows=table_rows)

@statistics.route('/save_example_table/', methods=['GET', 'POST'])
@login_required
def save_example_table ():
    if request.method == 'POST':
        name = request.form['name']
        serial_key = request.form['serial_key']
        table_example = request.form['table_example']
        head, rows = table_example.split('\n', 1)
        StatisticalTable.save(serial_key, head, rows, name, session.get('userid'))
        return render_template('save_example_table.html')


def _allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']
