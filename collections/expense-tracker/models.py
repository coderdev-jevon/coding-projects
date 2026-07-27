from collections import deque
from datetime import datetime, timedelta
from utils import parse_date

def calculate_total(amount: int, cost: float) -> float:
    return amount * cost

def filter_expenses_in_date_range(expenses: list, cutoff: int):
    now = datetime.now()
    # Find the date minimum point
    date_min = now - timedelta(days=cutoff)
    filtered_expenses = []
    data_list = expenses

    for data in data_list:
        if parse_date(data["date"]) >= date_min:
            filtered_expenses.append(data)
    return filtered_expenses

def get_latest_expenses(expenses: list, limit: int):
    # Set limit to deque collection
    dq = deque(maxlen=limit)
    sorted_expenses = sorted(expenses, key=lambda x: parse_date(x["date"]), reverse=True)

    for expense in sorted_expenses:
        dq.append(expense)

    return list(dq)
    