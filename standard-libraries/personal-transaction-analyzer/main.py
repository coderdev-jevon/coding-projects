from collections import namedtuple, deque, Counter
from database import read_logs
from itertools import groupby
import statistics as st
from models import parse_date

# Create namedtuple to store each log
LogRecord = namedtuple("LogRecord", ["date", "trans_type", "category", "description", "cost"])
# Storage created to store all of the logs in namedtuple type
logs_storage = []
logs = read_logs()

# Append each log to main storage
for log in logs:
    individual_log = LogRecord(
        date=parse_date(log[0]),
        trans_type=log[1],
        category=log[2],
        description=log[3],
        cost=int(log[4])
    )
    logs_storage.append(individual_log)

# Sort logs by date to get recent 15 logs
sorted_logs_by_date = sorted(logs_storage, key=lambda x: x.date)
top_15_logs = deque(sorted_logs_by_date, maxlen=15)
# Count number of spending times per category
spendings_counter = Counter([log.category for log in logs_storage])
category_mode = spendings_counter.most_common(1)

#Sort logs by expense and income before grouping to two groups
sorted_logs_by_transtype = sorted(logs_storage, key=lambda x: x.trans_type)
group_by_transtype = groupby(sorted_logs_by_transtype, key=lambda x: x.trans_type)
group_by_transtype = {group_key: list(items) for group_key, items in group_by_transtype}
# Group into expenses and incomes
expenses = group_by_transtype.get("expense", [])
incomes = group_by_transtype.get("income", [])

# Sort logs by category before grouping
sorted_logs_by_category = sorted(logs_storage, key=lambda x: x.category)
# Group logs by category
group_by_category = groupby(sorted_logs_by_category, key=lambda x: x.category)
# Limit focus to spendings only
per_category_spendings = {group_key: [item.cost] for group_key, items in group_by_category for item in items}
# Find average spendings per group
per_category_spendings_avg = {group_key: st.mean(values) for group_key, values in per_category_spendings.items()}
# Find the median spendings per group
per_category_spendings_median = {group_key: st.median(values) for group_key, values in per_category_spendings.items()}
