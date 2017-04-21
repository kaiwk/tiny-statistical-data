import io

from flask import (Blueprint, render_template, request,
                   flash, redirect, session, g, send_file)

from website import app
from website.views.account import login_required
from website.models.user import User
from website.models.statistical_table import StatisticalTable
from website.models.statistical_table_item import StatisticalTableItem

from website.ext.csv_parser import csv_parser

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
        g.statistical_table_id = statistical_table.tableid

        # get head and sample rows
        tablename, head, rows = _get_table_info(statistical_table)

        return render_template('fill_in_table.html',
                               tablename=tablename,
                               head=head,
                               rows=rows)

    # save table item
    if request.method == 'POST':

        # get head and sample rows
        tableid = request.form['tableid']
        statistical_table = StatisticalTable.get_statistical_table_by_table_id(tableid)

        tablename, head, rows = _get_table_info(statistical_table)

        # save
        fillin = request.form.to_dict()
        fillin_row = [fillin[h] for h in head]
        content = ','.join(fillin_row)

        StatisticalTableItem.save(tableid, content)

        return render_template('fill_in_table.html',
                               tablename=tablename,
                               head=head,
                               rows=rows,
                               fillin_row=fillin_row)


def _get_table_info(statistical_table):
    tablename = statistical_table.name
    head = statistical_table.head
    sample = statistical_table.sample
    csv_str = '\n'.join((head, sample))
    temp = csv_parser.get_lines(csv_str)
    head = temp[0]
    rows = temp[1:]
    return tablename, head, rows


@statistics.route('/publish_table/', methods=['GET', 'POST'])
@login_required
def publish_table():
    if request.method == 'GET':
        return render_template('publish_table.html')

    # check if the post request has the file part
    if 'uploaded-file' not in request.files:
        flash('No file part')
        return redirect(request.url)

    # if user does not select file, browser also
    # submit a empty part without filename
    file = request.files['uploaded-file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    # get csv file
    if file and _allowed_file(file.filename):
        utf8_converted_str = file.stream.read().decode('utf-8')
        temp = csv_parser.get_lines(utf8_converted_str)
        table_head = temp[0]
        table_rows = temp[1:]
        g.table_example = utf8_converted_str
        return render_template('publish_table.html',
                               table_head=table_head,
                               table_rows=table_rows)

@statistics.route('/save_example_table/', methods=['GET', 'POST'])
@login_required
def save_example_table():
    if request.method == 'POST':
        name = request.form['name']
        # TODO: auto generate serial key
        serial_key = request.form['serial_key']
        table_example = request.form['table_example']
        head, rows = table_example.split('\n', 1)
        StatisticalTable.save(serial_key, head, rows, name, session.get('userid'))
        return render_template('save_example_table.html')


def _allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@statistics.route('/show_all_tables/', methods=['GET'])
@login_required
def show_all_tables():
    userid = session.get('userid')
    tables = StatisticalTable.get_statistical_tables_by_user_id(userid)
    return render_template('show_all_tables.html', tables=tables)

@statistics.route('/show_table_detail/<int:tableid>', methods=['GET', 'POST'])
@login_required
def show_table_detail(tableid):
    table = StatisticalTable.get_statistical_table_by_table_id(tableid)
    session['tableid'] = table.tableid
    items = StatisticalTableItem.get_all_items_by_statistical_table_id(tableid)
    tablehead = table.head.split(',')
    all_rows = [item.content.split(',') for item in items]
    return render_template('show_table_detail.html',
                           tablename=table.name,
                           tablehead=tablehead,
                           all_rows=all_rows)


@statistics.route('/download_table/', methods=['POST'])
@login_required
def download_table():
    if request.method == 'POST':
        tableid = session.get('tableid')
        table = StatisticalTable.get_statistical_table_by_table_id(tableid)
        items = StatisticalTableItem.get_all_items_by_statistical_table_id(tableid)
        all_rows = [item.content for item in items]
        csv_content = table.head + '\n' + csv_parser.get_content(all_rows)
        byteIO = io.BytesIO()
        byteIO.write(csv_content.encode())
        byteIO.seek(0)
        return send_file(byteIO,
                         attachment_filename=table.name+'.csv',
                         as_attachment=True)
