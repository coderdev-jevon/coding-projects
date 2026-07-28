from datetime import date
import random
def build_random_date(year, month, max_day):
    return date(year=year, month=month, day=random.randint(1, max_day)) 

def random_date(year, month):
    if year <= 0:
        return None
    if month not in range(1, 13):
        return None

    if month in [1,3,5,7,8,10,12]:
        return build_random_date(year, month, 31)
    elif month in [4,6,9,11]:
        return build_random_date(year, month, 30)
    elif month == 2:
        if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
            return build_random_date(year, month, 29)
        return build_random_date(year, month, 28)

def random_cost(min_total, max_total):
    min = min_total
    max = max_total

    # Floor divide by 100 and multiply by 100 at the end to make it divisible by 100
    min_base = min // 100
    max_base = max // 100

    base = random.randint(min_base, max_base)
    return base * 100