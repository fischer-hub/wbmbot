import time, datetime
from argparse import ArgumentParser


def date():
    return datetime.datetime.fromtimestamp(time.time()).strftime('%d.%m.%Y - %H:%M')


def already_applied(flat, log_file_path='log1.txt'):

    with open(log_file_path, "r") as log_file:
        log = log_file.read()

    return str(flat.hash) in log


def filter_triggered(flat, user):
    
    return (user.filter[0] and any(str(keyword).strip() in flat.text().lower() for keyword in user.filter))


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
    parser.add_argument("-x", "--experimental", action='store_true', help="If set, turn on experimental mode. This could help increase the chance to get an appointment to view a flat, however, it could also get you banned.. (read up on this in the README) ")
    parser.add_argument("-i", "--interval", default=5, help="Set the time interval in minutes to check for new flats on wbm.de. [default: 5]")
    parser.add_argument("-l", "--latency_wait", default=1.5, help="Set time to wait after interaction with website. Slow connections might need a higher latency-wait-time. [default: 1.5s]")
    parser.add_argument("-y", "--yaml", default='config.yaml', help= "Provide configuration file name to load config from.[default: 'config.yaml']")
    parser.add_argument("-o", "--log", default='log.txt', help="Provide log file name to write log data to. [default: 'log.txt']")
    return parser.parse_args()

def console_log(self, msg):
    if msg:
        if self.cli:
            print(f"[{date()}] {msg}")
        else:
            self.console_out_sig.emit(f"[{date()}] {msg}")

def cheat(user, real_fname, real_lname, idx):
    if idx > 0:
        if idx < len(real_fname)-1:
            a = real_fname[idx]
            b = real_fname[idx+1]
            user.first_name = real_fname[:idx] + b + a if idx == len(real_fname)-2 else real_fname[:idx] + b + a + real_fname[idx+2:]
            return user

        elif (idx - len(real_fname)) < len(real_lname)-3:
            a = real_lname[idx-len(real_fname)+2]
            b = real_lname[idx-len(real_fname)+3]
            user.last_name = real_lname[:idx-len(real_fname)+1] + b + a if (idx - len(real_fname))-1 == len(real_lname)-3 else real_lname[:idx-len(real_fname)+2] + b + a + real_lname[idx-len(real_fname)+4:]
            user.first_name = real_fname

            return user
    
    user.last_name = real_lname
    return user
