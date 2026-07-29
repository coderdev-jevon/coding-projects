from datetime import date
import random as rnd

def build_random_date(year: int, month: int, day: int):
    return date(year=year, month=month, day=day)

def random_date(year: int):
    month = rnd.randint(1,12)

    if month in [1,3,5,7,8,10,12]:
        return build_random_date(year, month, 31)
    elif month in [4,6,9,11]:
        return build_random_date(year, month, 30)
    elif month == 2:
        if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
            return build_random_date(year, month, 29)
        return build_random_date(year, month, 28)

def random_duration(min_time, max_time):
    min_base = min_time // 10
    max_base = max_time // 10

    base = rnd.randint(min_base, max_base)
    return base * 10

def parse_date(date_string):
    return date.strptime(date_string, '%Y-%m-%d')