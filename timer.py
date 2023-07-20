import datetime


def time_difference(latest_time, days, hours, minutes):
    new_time = datetime.timedelta(days=days, hours=hours, minutes=minutes)
    return new_time
