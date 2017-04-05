from flask import (Blueprint, request, jsonify, abort, make_response)

from website.models.user import User
from website.models.statistical_table import StatisticalTable
from website.models.statistical_table_item import StatisticalTableItem

apiv1 = Blueprint('apiv1.0', __name__, url_prefix='/apiv1.0')

@apiv1.route('/get_table_info/<serial_key>/', methods=['GET'])
def get_table_info(serial_key):
    statistical_table = StatisticalTable.get_statistical_table_by_serial_key(serial_key)
    return jsonify(statistical_table.__dict__())


@apiv1.route('/get_table_items/<tableid>/', methods=['GET'])
def get_table_items(tableid):
    items = StatisticalTableItem.get_all_items_by_statistical_table_id(tableid)
    all_items = [item.__dict__() for item in items]
    return jsonify({'all_items': all_items})

@apiv1.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@apiv1.route('/fill_in_table/', methods=['POST'])
def fill_table():
    if not request.json or not 'tableid' in request.json:
        abort(404)
    tableid = request.json['tableid']
    serial_key = request.json['serial_key']
    content = request.json['content']

    statistical_table = StatisticalTable.get_statistical_table_by_table_id(tableid)

    if serial_key != statistical_table.serial_key:
        return jsonify({'status': 400, 'log': 'bad request'})

    StatisticalTableItem.save(tableid, content)
    return jsonify({'status': 200})
