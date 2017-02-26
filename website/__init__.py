from flask import Flask, g

import json
import os

from .ext.flask_mysql.mysql import MySQL
from werkzeug.local import LocalProxy

_app = Flask(__name__, instance_relative_config=True)
_app.secret_key = 'this is a screte key!'

# database
# MySQL configurations
with open(os.path.join(_app.instance_path, '_private_config.json'), 'r') as f:
    config = json.load(f)
    _app.config['MYSQL_DATABASE_USER'] = config['MYSQL_DATABASE_USER']
    _app.config['MYSQL_DATABASE_PASSWORD'] = config['MYSQL_DATABASE_PASSWORD']
    _app.config['MYSQL_DATABASE_DB'] = config['MYSQL_DATABASE_DB']
    _app.config['MYSQL_DATABASE_HOST'] = config['MYSQL_DATABASE_HOST']
_app.config['MYSQL_CURSOR_CLASS'] = 'dictcursor'

db = LocalProxy(MySQL(_app).get_db)

# blueprint
def register_blueprint():
    from .views.account import account
    from .views.statistics import statistics
    _app.register_blueprint(account)
    _app.register_blueprint(statistics)
    return _app

__all__ = [
    'register_blueprint',
    'db'
]
