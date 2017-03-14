from website import db


class StatisticalTable(object):
    def __init__(self):
        self.serial_key = None
        self.head = None
        self.sample = None
        self.name = None
        self.user_id = None


    @staticmethod
    def save(serial_key, head, sample, name, user_id):

        pass

    @staticmethod
    def get_statistical_table_by_user_id(user_id):
        pass
