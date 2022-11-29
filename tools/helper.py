import os

from tools.constants import INTERVALS


def display_time(seconds, granularity=2):
    result = []

    for name, count in INTERVALS:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip("s")
            result.append("{} {}".format(value, name))
    if len(result) == 0:
        result.append("0 seconds")
    return ", ".join(result[:granularity])


def get_ip():
    return "localhost" if get_debug() else "0.0.0.0"
    return "localhost" if os.name == "nt" else "192.168.178.100"


def get_debug():
    return True if os.name == "nt" else False
