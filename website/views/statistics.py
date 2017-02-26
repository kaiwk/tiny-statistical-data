from flask import (Blueprint, render_template, request,
                   flash, redirect, url_for, session)

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
