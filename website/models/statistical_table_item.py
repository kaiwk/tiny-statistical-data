from website import db


class StatisticalTableItem(object):

    def __init__(self, itemInfo):
        self.order_num = None
        self.content = None
        self.statistical_table_id = None

        if itemInfo:
            self.order_num = itemInfo['order_num']
            self.content = itemInfo['content']
            self.statistical_table_id = itemInfo['statistical_table_id']

    @classmethod
    def get_all_items_by_statistical_table_id(cls, table_id):
        cursor = db.cursor()
        cursor.execute(
            'select order_num, content, statistical_table_id from statistical_tablel_item where statistical_table_id = %s',
            (table_id,))
        fetch_res = cursor.fetchall()
        items = []
        for e in fetch_res:
            items.append(cls(e))
        return items

    @staticmethod
    def save (order_num, content, statistical_table_id):
        cursor = db.cursor()
        cursor.execute(
            'insert into statistical_table_item  (order_num, content, statistical_table_id) value (%s, %s, %s)',
            (order_num, content, statistical_table_id))
        db.commit()

    @staticmethod
    def get_count():
        cursor = db.cursor()
        cursor.execute(
            'select count(*) from statistical_table_item'
        )
        return cursor.fetchone()['count(*)']
