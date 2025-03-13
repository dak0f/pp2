from datetime import datetime

date1 = datetime(2023, 10, 1, 12, 0, 0) 
date2 = datetime(2023, 10, 5, 12, 0, 0)  
difference_in_seconds = (date2 - date1).total_seconds()

print("Date 1:", date1)
print("Date 2:", date2)
print("Difference in seconds:", difference_in_seconds)