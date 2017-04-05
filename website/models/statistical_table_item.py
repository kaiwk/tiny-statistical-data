from website import db


class StatisticalTableItem(object):

    def __init__(self, itemInfo):
        self.content = None
        self.statistical_table_id = None

        if itemInfo:
            self.content = itemInfo['content']
            self.statistical_table_id = itemInfo['statistical_table_id']

    @classmethod
    def get_all_items_by_statistical_table_id(cls, table_id):
        cursor = db.cursor()
        cursor.execute(
            'select content, statistical_table_id from statistical_table_item where statistical_table_id = %s',
            (table_id,))
        fetch_res = cursor.fetchall()
        items = [cls(row) for row in fetch_res]
        return items

    @staticmethod
    def save (statistical_table_id, content):
        cursor = db.cursor()
        cursor.execute(
            'insert into statistical_table_item (content, statistical_table_id) value (%s, %s)',
            (content, statistical_table_id))
        db.commit()

    @staticmethod
    def get_count():
        cursor = db.cursor()
        cursor.execute(
            'select count(*) from statistical_table_item'
        )
        return cursor.fetchone()['count(*)']


    def __dict__(self):
        return {
            'content': self.content,
            'statistical_table_id': self.statistical_table_id
        }
