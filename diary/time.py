from datetime import datetime

now = datetime.now()
date_time = now.strftime("%Y-%m-%d-%H-%M-%S")

filename = f'file-{date_time}'

print(date_time)
print(filename)
