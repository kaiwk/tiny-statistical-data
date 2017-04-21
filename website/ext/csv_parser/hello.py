from .csv_parser import get_content

lines = [['name', 'age', 'grade', 'score'], ['Larry', '21', '13', '92']]
csv_str = get_content(lines)

print(csv_str)
