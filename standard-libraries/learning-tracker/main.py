from collections import namedtuple, deque
from database import read_logs
from itertools import groupby
import statistics as st
from utils import parse_date

# Create database structure in namedtuple to store each log's data
LearningRecord = namedtuple("LearningRecord", ["date", "topic", "duration"])

def analyze_learning_logs():
    # Read the learning logs
    learning_logs = read_logs('learning_2026.log')

    # Main storage for learning logs
    learning_records = []

    # Store the data to main storage
    for log in learning_logs:
        # Check the length of the list, ideally it is 3
        if len(log) != 3:
            continue
        # Check the validity of each log
        try:
            date_string = parse_date(log[0])
            # Check if date_string returns
            if date_string is None:
                continue
            topic = log[1]
            if not topic:
                continue
            duration = int(log[2])
        except (ValueError, TypeError):
            continue
        # Store into temporary tuple and append to main storage
        tmp = LearningRecord(
            date=date_string,
            topic=topic,
            duration=duration
        )
        learning_records.append(tmp)

    # Sort by date and get top 15 newest logs
    sorted_by_date = sorted(learning_records, key=lambda x: x.date)
    top_15_most_recent_logs = deque(sorted_by_date, maxlen=15)

    # Sort and Group records by topic
    sorted_by_topic = sorted(learning_records, key=lambda x: x.topic)
    groupby_topic = groupby(sorted_by_topic, key=lambda x: x.topic)

    # Per topic durations, avg duration, median duration
    duration_per_topic = {}
    for group_key, items in groupby_topic:
        durations = [item.duration for item in items]
        # Check if empty
        if not durations:
            continue
        duration_per_topic[group_key] = {
            "duration": durations,
            "duration_avg": st.mean(durations),
            "duration_median": st.median(durations)
        }
    return learning_records, top_15_most_recent_logs, duration_per_topic

if __name__ == '__main__':
    records, recent, topic_stats = analyze_learning_logs()
    print(topic_stats)
