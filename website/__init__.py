import json
import os

from flask import Flask, g
from website.ext.flask_mysql.mysql import MySQL
from werkzeug.local import LocalProxy

app = Flask(__name__, instance_relative_config=True)
app.secret_key = 'this is a screte key!'

# database
# MySQL configurations
with open(os.path.join(app.instance_path, 'config', '_private_config.json'), 'r') as f:
    config = json.load(f)
    app.config['MYSQL_DATABASE_USER'] = config['MYSQL_DATABASE_USER']
    app.config['MYSQL_DATABASE_PASSWORD'] = config['MYSQL_DATABASE_PASSWORD']
    app.config['MYSQL_DATABASE_DB'] = config['MYSQL_DATABASE_DB']
    app.config['MYSQL_DATABASE_HOST'] = config['MYSQL_DATABASE_HOST']
app.config['MYSQL_CURSOR_CLASS'] = 'dictcursor'

db = LocalProxy(MySQL(app).get_db)

app.config['ALLOWED_EXTENSIONS'] = set(['csv'])
app.config['UPLOAD_FOLDER'] = os.path.join(app.instance_path, 'upload')

# blueprint
def register_blueprint():
    from website.views.account import account
    from website.views.statistics import statistics
    from website.api.apiv1 import apiv1
    app.register_blueprint(account)
    app.register_blueprint(statistics)
    app.register_blueprint(apiv1)
    return app

__all__ = [
    'register_blueprint',
    'app',
    'db'
]
