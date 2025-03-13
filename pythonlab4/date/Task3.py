from datetime import datetime

current_datetime = datetime.now()

datetime_without_microseconds = current_datetime.replace(microsecond=0)

print(current_datetime)
print(datetime_without_microseconds)