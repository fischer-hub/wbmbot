# worker.py
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
import time, os
from src.user import User
from src import utils
from src.engine.init import init
from src.engine.interact import *
from src.engine import cli_setup

class Args():
    def __init__(self, h, t, o, l, i):
        self.headless_off = h
        self.test = t
        self.log = o
        self.latency_wait = l
        self.interval = i


class Worker(QObject):
    finished = pyqtSignal()
    console_out_sig = pyqtSignal(str)
    headless_off = True
    test = False
    interval = 5
    running = False
    user = User()
    var = ''
    latency = 1.5
    cli = False
    experimental = False
    yaml = ''
    log = 'log.txt'


    @pyqtSlot()
    def run(self):

        self.args = Args(self.headless_off, self.test, self.log, self.latency, self.interval)

        user, flat, start_url, driver, page_changed, curr_page_num = init(self.args)


        if self.cli:
            
            if not os.path.isfile(self.yaml):

                utils.console_log(self, f"No config file found, starting setup..")

                cli_setup.setup(self.yaml)


            utils.console_log(self, "Loading config..")

            user.parse_config_file(self.yaml)


        while self.running:


            if not page_changed:
                
                utils.console_log(self, f"Connecting to {start_url} ..")
                driver.get(start_url)
                curr_page_num = 1
                prev_page_num = 1


            utils.console_log(self, f"{accept_cookies(driver, float(self.latency))}")
            
            utils.console_log(self, "Looking for flats..")
            
            
            if scrape_flats(driver):
                
                utils.console_log(self, f"Found {len(scrape_flats(driver))} flat(s) in total:")


                for i in range(0,len(scrape_flats(driver))):
                    
                    flat.parse_flat_elem(scrape_flats(driver)[i])


                    if utils.already_applied(flat, self.args.log):

                        utils.console_log(self, f"Oops, we already applied for flat: {flat.title}!")

                    elif utils.filter_triggered(flat, user):

                        utils.console_log(self, f"Ignoring flat '{flat.title}' because it contains filter keyword(s).")
                    
                    else:

                        utils.console_log(self, f"Applying for flat: {flat.title}..")

                        real_fname = user.first_name

                        real_lname = user.last_name


                        for idx, email in enumerate(user.email):

                            if self.experimental: 
                                
                                utils.cheat(user, real_fname, real_lname, idx)

                            utils.console_log(self, f"Applying with name: {user.first_name} {user.last_name}..")
                            
                        
                            click_continue(scrape_flats(driver)[i], driver, float(self.latency))

                            fill_form(email, driver, user, float(self.latency))

                            submit_and_go_back(driver, float(self.latency))


                        user.first_name = real_fname

                        user.last_name = real_lname

                        utils.log_flat(flat, self.args.log)


                    if i == len(scrape_flats(driver))-1: 
                        prev_page_num = curr_page_num
                        curr_page_num = next_page(curr_page_num, driver, float(self.latency))
                        page_changed = curr_page_num != prev_page_num


            else:

                utils.console_log(self, f"Currently no flats available :(")


            if not self.running: break

            if not page_changed:
                
                for i in range(0,60):
                    if not self.running: break
                    time.sleep(float(self.args.interval))

                utils.console_log(self, f"Reloading main page..")
            
            else:
            
                time.sleep(1.5)

        driver.quit()
        self.finished.emit()

            

