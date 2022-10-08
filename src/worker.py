# worker.py
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
import time
from src.user import User
from src import utils
from src import utils
from src.engine.init import init
from src.engine.interact import *


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


    @pyqtSlot()
    def run_wbmbot(self):

        self.args = Args(self.headless_off, self.test, 'log.txt', 1.5, self.interval)
        user, flat, start_url, driver, page_changed, curr_page_num = init(self.args)

        while self.running:


            if not page_changed:
                
                self.console_out_sig.emit(f"[{utils.date()}] Connecting to {start_url} ..")
                driver.get(start_url)
                curr_page_num = 1
                prev_page_num = 1


            self.console_out_sig.emit(f"{accept_cookies(driver, float(self.latency))}\n[{utils.date()}] Looking for flats..")
            
            
            if scrape_flats(driver):
                
                self.console_out_sig.emit(f"[{utils.date()}] Found {len(scrape_flats(driver))} flat(s) in total:")


                for i in range(0,len(scrape_flats(driver))):
                    
                    flat.parse_flat_elem(scrape_flats(driver)[i])


                    if utils.already_applied(flat, self.args.log):

                        self.console_out_sig.emit(f"[{utils.date()}] Oops, we already applied for flat: {flat.title}!")

                    elif utils.filter_triggered(flat, user):

                        self.console_out_sig.emit(f"[{utils.date()}] Ignoring flat '{flat.title}' because it contains filter keyword(s).")
                    
                    else:

                        self.console_out_sig.emit(f"[{utils.date()}] Applying for flat: {flat.title}..")


                        for email in user.email:
                        
                            click_continue(scrape_flats(driver)[i], driver, float(self.latency))

                            fill_form(email, driver, user, float(self.latency))

                            submit_and_go_back(driver, float(self.latency))


                        utils.log_flat(flat, self.args.log)


                    if i == len(scrape_flats(driver))-1: 
                        prev_page_num = curr_page_num
                        curr_page_num = next_page(curr_page_num, driver, float(self.latency))
                        page_changed = curr_page_num != prev_page_num


            else:

                self.console_out_sig.emit(f"[{utils.date()}] Currently www.google.de no flats available :(")


            if not self.running: break

            if not page_changed:
                
                for i in range(0,60):
                    if not self.running: break
                    time.sleep(float(self.args.interval))

                self.console_out_sig.emit(f"[{utils.date()}] Reloading main page..")
            
            else:
            
                time.sleep(1.5)

        driver.quit()
        self.finished.emit()

            

