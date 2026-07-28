from datetime import date

def extract_year_month(filename):
    # remove .log / .txt extension
    name_no_extension = filename.split('.')[0]
    parts = name_no_extension.split('_')
    # part[0] = transaction, part[1] = year, part[2] = month
    year = int(parts[1])
    month = int(parts[2])
    return year, month

def parse_date(date_string):
    return date.strptime(date_string, '%Y-%m-%d')