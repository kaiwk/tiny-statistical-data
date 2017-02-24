from __future__ import absolute_import
import pymysql

from flask import g

class MySQL(object):
    def __init__(self, app=None, **connect_args):
        self.connect_args = connect_args
        self.cursorclass = {
            'cursor': pymysql.cursors.Cursor,
            'sscursor': pymysql.cursors.SSCursor,
            'dictcursor': pymysql.cursors.DictCursor,
            'ssdictcursor': pymysql.cursors.SSDictCursor
        }
        if app is not None:
            self.app = app
            self.init_app(self.app)
        else:
            self.app = None

    def init_app(self, app):
        self.app = app
        self.app.config.setdefault('MYSQL_DATABASE_HOST', 'localhost')
        self.app.config.setdefault('MYSQL_DATABASE_PORT', 3306)
        self.app.config.setdefault('MYSQL_DATABASE_USER', None)
        self.app.config.setdefault('MYSQL_DATABASE_PASSWORD', None)
        self.app.config.setdefault('MYSQL_DATABASE_DB', None)
        self.app.config.setdefault('MYSQL_DATABASE_CHARSET', 'utf8mb4')
        self.app.config.setdefault('MYSQL_USE_UNICODE', True)
        self.app.config.setdefault('MYSQL_CURSOR_CLASS', 'cursor')
        #Flask 0.9 or later
        if hasattr(app, 'teardown_appcontext'):
            self.app.teardown_request(self.teardown_request)
        #Flask 0.7 to 0.8
        elif hasattr(app, 'teardown_request'):
            self.app.teardown_request(self.teardown_request)
        #Older versions
        else:
            self.app.after_request(self.teardown_request)

    def connect(self):
        if self.app.config['MYSQL_DATABASE_HOST']:
            self.connect_args['host'] = self.app.config['MYSQL_DATABASE_HOST']
        if self.app.config['MYSQL_DATABASE_PORT']:
            self.connect_args['port'] = self.app.config['MYSQL_DATABASE_PORT']
        if self.app.config['MYSQL_DATABASE_USER']:
            self.connect_args['user'] = self.app.config['MYSQL_DATABASE_USER']
        if self.app.config['MYSQL_DATABASE_PASSWORD']:
            self.connect_args['password'] = self.app.config['MYSQL_DATABASE_PASSWORD']
        if self.app.config['MYSQL_DATABASE_DB']:
            self.connect_args['db'] = self.app.config['MYSQL_DATABASE_DB']
        if self.app.config['MYSQL_DATABASE_CHARSET']:
            self.connect_args['charset'] = self.app.config['MYSQL_DATABASE_CHARSET']
        if self.app.config['MYSQL_USE_UNICODE']:
            self.connect_args['use_unicode'] = self.app.config['MYSQL_USE_UNICODE']
        if self.app.config['MYSQL_CURSOR_CLASS']:
            self.connect_args['cursorclass'] = self.cursorclass[self.app.config['MYSQL_CURSOR_CLASS']]
        return pymysql.connect(**self.connect_args)

    def teardown_request(self, exception):
        db = getattr(g, '_database', None)
        if db is not None:
            db.close()

    def get_db(self):
        db = getattr(g, '_database', None)
        if db is None:
            db = g._database = self.connect()
        return db
