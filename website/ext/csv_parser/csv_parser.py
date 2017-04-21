import csv
import io

def get_lines(csv_str):
    csvlist = csv.reader(io.StringIO(csv_str), skipinitialspace=True)
    temp = [line for line in csvlist]
    return temp

def get_content(lines):
    ret = '\n'.join(lines)
    return ret
