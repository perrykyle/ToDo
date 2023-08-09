from datetime import datetime, timedelta, timezone


def convert_to_est(utc_string):
    utc_time = datetime.strptime(utc_string, '%Y-%m-%d %H:%M:%S')
    est_time = utc_time.replace(tzinfo=timezone.utc).astimezone(timezone(timedelta(hours=-4)))
    formatted_est_time = est_time.strftime('%H:%M-%Y-%m-%d')
    return formatted_est_time


utc_string = '2023-08-09 03:00:00'
est_value = convert_to_est(utc_string)
print(est_value)  # Output:
