import datetime
import requests
import logging

logging.basicConfig(filename='log.log', encoding='utf-8', level=logging.INFO,
                    format='%(asctime)s %(message)s', datefmt='%Y/%m/%d %I:%M:%S %p')


def time_difference(latest_time, days, hours, minutes):
    latest_time = datetime.datetime.strptime(latest_time, '%Y-%m-%d %H:%M:%S')
    new_time = latest_time + datetime.timedelta(days=days, hours=hours, minutes=minutes)
    return new_time


def get_latest_version():
    try:
        response = requests.get("https://api.github.com/repos/kbkozlev/BinCleaner/releases/latest")
        latest_release = response.json()['tag_name']
        download_url = response.json()['html_url']

    except Exception as e:
        logging.error(e)
        latest_release = None
        download_url = None

    return latest_release, download_url
