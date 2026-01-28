
# """24-05-2004 18:03 + -6.7470217 working days -> 13-05-2004 10:02 (?)"""

from datetime import datetime, timedelta

remainder = 0.7470217
total_workday_seconds = 8 * 60 * 60 

seconds_to_subtract = remainder * total_workday_seconds

start_datetime = datetime(2004, 5, 24, 16, 0) # Starting point adjusted to workday end time

final_datetime = start_datetime - timedelta(seconds=seconds_to_subtract)

print("Remainder", remainder)
print("Total workday seconds:", total_workday_seconds)
print("Seconds to subtract:", seconds_to_subtract)
print("Initial datetime:", start_datetime)
print("Final time:", final_datetime.time())

# --- Output ---
# Remainder 0.7470217
# Total workday seconds: 28800
# Seconds to subtract: 21514.22496
# Initial datetime: 2004-05-24 16:00:00
# Final time: 10:01:25.775040