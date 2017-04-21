import unittest

from website.ext.csv_parser import csv_parser

class CSVParserTestCase(unittest.TestCase):

    def test_get_lines(self):
        csv_str = 'name,age,grade,score\nLarry,21,13,92'
        lines = csv_parser.get_lines(csv_str)
        assert lines == [['name', 'age', 'grade', 'score'], ['Larry', '21', '13', '92']], \
            'csv_parser: get_lines: error'

        csv_str = 'name, age, grade, score\nLarry, 21, 13, 92'
        lines = csv_parser.get_lines(csv_str)
        assert lines == [['name', 'age', 'grade', 'score'], ['Larry', '21', '13', '92']], \
            'csv_parser: get_line: not strip the whitespace'

    def test_get_content(self):
        lines = ['name,age,grade,score', 'Larry,21,13,92']
        csv_str = csv_parser.get_content(lines)
        assert csv_str == 'name,age,grade,score\nLarry,21,13,92', \
            'csv_parser: get_content: error'
