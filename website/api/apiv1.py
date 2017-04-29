from flask import (Blueprint, request, jsonify, abort, make_response)

from website.models.statistical_table import StatisticalTable
from website.models.statistical_table_item import StatisticalTableItem

apiv1 = Blueprint('apiv1.0', __name__, url_prefix='/apiv1.0')

@apiv1.route('/get_table_info/<serial_key>/', methods=['GET'])
def get_table_info(serial_key):
    statistical_table = StatisticalTable.get_statistical_table_by_serial_key(serial_key)
    return jsonify(statistical_table.__dict__())


@apiv1.route('/get_table_items/<serial_key>/', methods=['GET'])
def get_table_items(serial_key):
    table = StatisticalTable.get_statistical_table_by_serial_key(serial_key)
    items = StatisticalTableItem.get_all_items_by_statistical_table_id(table.tableid)
    all_items = [item.__dict__() for item in items]
    return jsonify({'all_items': all_items})

@apiv1.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@apiv1.route('/fill_in_table/', methods=['POST'])
def fill_table():
    if not request.form or not 'serial_key' in request.form:
        abort(404)
    serial_key = request.form['serial_key']
    content = request.form['content']
    statistical_table = StatisticalTable.get_statistical_table_by_serial_key(serial_key)

    if serial_key != statistical_table.serial_key:
        return jsonify({'status': 400, 'log': 'bad request'})

    StatisticalTableItem.save(statistical_table.tableid, content)
    return jsonify({'status': 200})
