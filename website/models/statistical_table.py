from website import db


class StatisticalTable(object):

    def __init__(self, tableinfo):
        self.tableid = None
        self.serial_key = None
        self.head = None
        self.sample = None
        self.name = None
        self.user_id = None
        self.create_time = None
        self.update_time = None

        if tableinfo:
            self.tableid = tableinfo['tableid']
            self.serial_key = tableinfo['serial_key']
            self.head = tableinfo['head']
            self.sample = tableinfo['sample']
            self.name = tableinfo['name']
            self.user_id = tableinfo['user_id']

    @staticmethod
    def save(serial_key, head, sample, name, user_id):
        cursor = db.cursor()
        cursor.execute(
            'insert into statistical_table (serial_key, head, sample, name, user_id) values (%s, %s, %s, %s, %s)',
            (serial_key, head, sample, name, user_id))
        db.commit()

    @classmethod
    def get_statistical_tables_by_user_id(cls, user_id):
        cursor = db.cursor()
        cursor.execute(
            'select id as tableid, serial_key, head, sample, name, user_id \
            from statistical_table where user_id=%s',
            (user_id,))
        fetch_res = cursor.fetchall()
        tables = [cls(row) for row in fetch_res]
        return tables

    @classmethod
    def get_statistical_table_by_serial_key(cls, serial_key):
        cursor = db.cursor()
        cursor.execute(
            'select id as tableid, serial_key, head, sample, name, user_id \
            from statistical_table where serial_key=%s',
            (serial_key,)
        )
        fetch_res = cursor.fetchone()
        return cls(fetch_res)

    @classmethod
    def get_statistical_table_by_table_id(cls, tableid):
        cursor = db.cursor()
        cursor.execute(
            'select id as tableid, serial_key, head, sample, name, user_id \
            from statistical_table where id=%s',
            (tableid,)
        )
        fetch_res = cursor.fetchone()
        return cls(fetch_res)
