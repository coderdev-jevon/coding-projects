from config import folder, LEARNING_TOPICS
from datetime import date
from utils import random_date, random_duration
from pathlib import Path
import random as rnd

# date, topic, duration
def write_random_logs(file_name, times: int):
    # Directing to the file path
    file = folder / Path(file_name)
    # Open the file
    with file.open('a', encoding='utf-8') as f:
        for i in range(times):
            # Generate random date
            day = random_date(2026)
            day_string = day.strftime('%Y-%m-%d')
            # Generate random topic from list
            topic = rnd.choice(LEARNING_TOPICS)
            # Generate random duration
            duration_string = str(random_duration(10, 500))

            # Combine date, topic, and duration into complete log and append
            complete_log = ",".join([day_string, topic, duration_string])
            f.write(complete_log + "\n")

def read_logs(file_name):
    # Directing to the file
    file = folder / Path(file_name)
    # Handle errors if file can't open
    try:
        with file.open('r', encoding='utf-8') as f:
            for line_raw in f:
                # Clean the line
                line = line_raw.strip()
                # If empty, skip the iteration
                if not line:
                    continue
                # Split parts by , and yield it
                parts = line.split(',')
                yield parts
    except IOError as e:
        print(f"Error Detected: {e}") 



