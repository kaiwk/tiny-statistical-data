from flask import Blueprint, render_template, request, flash, redirect, url_for

statistics = Blueprint('statistics',
                       __name__,
                       template_folder='../templates/statistics',
                       url_prefix='/statistics')

@statistics.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    serial_id = request.form['serial_id']
    # TODO: get sheet by serial id.
    return render_template('show_table_detail.html', serial_id=serial_id)


@statistics.route('/publish_table/', methods=['GET', 'POST'])
def publish_table():
    if request.method == 'GET':
        return render_template('publish_table.html')
