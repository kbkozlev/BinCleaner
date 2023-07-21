import datetime


def time_difference(latest_time, days, hours, minutes):
    latest_time = datetime.datetime.strptime(latest_time, '%Y-%m-%d %H:%M:%S')
    new_time = latest_time + datetime.timedelta(days=days, hours=hours, minutes=minutes)
    return new_time
