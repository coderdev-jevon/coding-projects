from pathlib import Path

def log_reader(file_path: str | Path):
    file_path = Path(file_path)
    try:
        with file_path.open('r', encoding='utf-8') as f:
            for line in f:
                stripped_line = line.strip()
                yield stripped_line
    except FileNotFoundError:
        print(f"File {file_path} is not found")

if __name__ == '__main__':
    logs = log_reader('app.log')
    for entry in logs:
        print(entry)