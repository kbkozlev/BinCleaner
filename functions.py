import datetime
import requests


def time_difference(latest_time, days, hours, minutes):
    latest_time = datetime.datetime.strptime(latest_time, '%Y-%m-%d %H:%M:%S')
    new_time = latest_time + datetime.timedelta(days=days, hours=hours, minutes=minutes)
    return new_time


def get_latest_version():
    try:
        response = requests.get("https://api.github.com/repos/kbkozlev/BinCleaner/releases/latest")
        latest_release = response.json()['tag_name']
        download_url = response.json()['html_url']

    except:
        latest_release = None
        download_url = None

    return latest_release, download_url
