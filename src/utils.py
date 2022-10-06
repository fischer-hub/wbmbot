import sys, time, datetime, hashlib, yaml, os.path

def date():
    return datetime.datetime.fromtimestamp(time.time()).strftime('%d.%m.%Y - %H:%M')