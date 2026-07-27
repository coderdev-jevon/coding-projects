from models import read_all_logs

logs = read_all_logs()
for log in logs:
    print(log)