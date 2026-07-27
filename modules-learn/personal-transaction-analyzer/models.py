from config import folder

def read_all_logs():
    log_files = folder.glob('*.log')
    for file in log_files:
        if not file.is_file():
            continue
        try:
            with file.open('r', encoding='utf-8') as f:
                for raw_line in f:
                    line = raw_line.strip()
                    if line:
                        yield line.split(',')
                        
        except IOError as err:
            print(f"Warning: cannot read {file.name}: {err}")