import time
import datetime


def str_to_timestamp(string, fmt="%Y-%m-%d %H:%M"):
    return time.mktime(datetime.datetime.strptime(string, fmt).timetuple())

def timestamp_to_date(ts):
    return datetime.datetime.fromtimestamp(ts)