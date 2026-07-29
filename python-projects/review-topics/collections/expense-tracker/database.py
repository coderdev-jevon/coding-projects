from config import FILENAME
import json

# Reading main json data
def load_data():
    if not FILENAME.exists():
        return []
    try:
        with FILENAME.open('r', encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        # File exists but content is broken / empty
        return []

# Overwriting main json data
def save_data(updated_data):
    with FILENAME.open('w', encoding='utf-8') as f:
        json.dump(updated_data, f, ensure_ascii=False, indent=4)
