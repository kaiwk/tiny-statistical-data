from flask import Flask, g
import flask_login

from .ext.flask_mysql.mysql import MySQL

_app = Flask(__name__)
_app.secret_key = 'this is a screte key!'

# flask-login
login_manager = flask_login.LoginManager()
login_manager.init_app(_app)

# database
def _create_db():
    # MySQL configurations
    _app.config['MYSQL_DATABASE_USER'] = 'root'
    _app.config['MYSQL_DATABASE_PASSWORD'] = '19951231'
    _app.config['MYSQL_DATABASE_DB'] = 'tiny_statistical_data'
    _app.config['MYSQL_DATABASE_HOST'] = 'localhost'
    _app.config['MYSQL_CURSOR_CLASS'] = 'dictcursor'
    return MySQL(_app)

db_helper = _create_db()

# blueprint
def register_blueprint():
    from .views.account import account
    from .views.statistics import statistics
    _app.register_blueprint(account)
    _app.register_blueprint(statistics)
    return _app

__all__ = [
    'register_blueprint',
    'login_manager'
]
