from config import folder, INCOME_CATEGORIES, EXPENSE_CATEGORIES, SAMPLE_DESCRIPTIONS
from datetime import date
from models import extract_year_month
from pathlib import Path
import random
from utils import random_date, random_cost

def read_logs():
    # get all log files
    files = folder.glob('*.log')
    for file in files:
        if not file.is_file():
            continue
        try:
            with file.open('r', encoding='utf-8') as f:
                for log_raw in f:
                    log = log_raw.strip()
                    parts = log.split(",")
                    # Yield back data from each log
                    yield parts
        # Prevent OS Error
        except IOError as e:
            print(f"File {file} is not available: e")

def write_random_logs(file_path: str, times: int):
    # directing to the file 
    file = folder / Path(file_path)
    # Open the file to append
    with file.open('a', encoding='utf-8') as f:
        for i in range(times):
        # Try and Except to prevent errors occured
            try: 
                # create random date
                y, m = extract_year_month(file_path)
                day = random_date(y, m)
                
                date_string = day.strftime('%Y-%m-%d')
                # random expense or income
                trans_type = random.choice(['income', 'expense'])
                # random categories
                if trans_type == 'income':
                    category = random.choice(INCOME_CATEGORIES)
                elif trans_type == "expense":
                    category = random.choice(EXPENSE_CATEGORIES)
                # random description from category
                description = random.choice(SAMPLE_DESCRIPTIONS.get(category, ["General Description"]))
                #random cost
                cost = random_cost(10000, 100000)
                cost_string = str(cost)

                # combine all values into one log
                complete_log = [date_string, trans_type, category, description, cost_string]
                # append to the file
                f.write(",".join(complete_log) + "\n")

            except (IOError, AttributeError) as e:
                print(f"Skip broken log: {e}")
                continue

write_random_logs('transaction_2026_05.log', 10)