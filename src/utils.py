import time, datetime
from argparse import ArgumentParser


def date():
    return datetime.datetime.fromtimestamp(time.time()).strftime('%d.%m.%Y - %H:%M')


def already_applied(flat, log_file_path='log1.txt'):

    with open(log_file_path, "r") as log_file:
        log = log_file.read()

    return str(flat.hash) in log


def filter_triggered(flat, user):
    
    return any(str(keyword).strip() in flat.text().lower() for keyword in user.filter)


def log_flat(flat, log_file_path='log.txt'):

    log_str = f"""
    [{date()}] - 
    Application sent for flat:
    Title: {flat.title}
    Address: {flat.street}
    {flat.city + ' ' + flat.zip_code}
    Total rent: {flat.total_rent}
    Flat size: {flat.size}
    Rooms: {flat.rooms}
    WBS: {flat.wbs}
    Hash: {flat.hash}\n\n
    """

    with open(log_file_path, "a") as log_file:
        log_file.write(log_str)

def arg_parse():
    parser = ArgumentParser()
    parser.add_argument("-c", "--cli", action='store_true', help="If set, run bot on command line only instead of starting the GUI.")
    parser.add_argument("-t", "--test", action='store_true', help="If set, run test-run on the test data. This does not actually connect to wbm.de.")
    parser.add_argument("-H", "--headless_off", action='store_false', help="If set, turn off headless run. The bot will run in the opened web browser.")
    parser.add_argument("-i", "--interval", default=5, help="Set the time interval in minutes to check for new flats on wbm.de. [default: 5]")
    parser.add_argument("-l", "--latency_wait", default=1.5, help="Set time to wait after interaction with website. Slow connections might need a higher latensy-wait-time. [default: 1.5s]")
    parser.add_argument("-y", "--yaml", default='config.yaml', help= "Provide configuration file name to load config from.[default: 'config.yaml']")
    parser.add_argument("-o", "--log", default='log.txt', help="Provide log file name to write log data to. [default: 'log.txt']")
    return parser.parse_args()