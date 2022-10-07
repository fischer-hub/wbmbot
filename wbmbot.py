#!/usr/bin/env python3

import sys, os, time
from PyQt5.QtWidgets import QApplication
from src.app import MainWindow
from src import utils
from src.engine.init import init
from src.engine.cli_setup import setup
from src.engine.interact import *


args = utils.arg_parse()


if args.cli:
    
    user, flat, start_url, driver, page_changed, curr_page_num = init(args)


    if not os.path.isfile(args.yaml):
        print(f"[{utils.date()}] No config file found, starting setup..")
        setup(args.yaml)

    print(f"[{utils.date()}] Loading config..")
    user.parse_config_file(args.yaml)


    while True:


        if not page_changed:
            
            print(f"[{utils.date()}] Connecting to {start_url} ..")
            driver.get(start_url)
            curr_page_num = 1
            prev_page_num = 1



        print(f"{accept_cookies(driver, float(args.latency_wait))}\n[{utils.date()}] Looking for flats..")
        
        
        if scrape_flats(driver):
            
            print(f"[{utils.date()}] Found {len(scrape_flats(driver))} flat(s) in total:")


            for i in range(0,len(scrape_flats(driver))):
                
                flat.parse_flat_elem(scrape_flats(driver)[i])


                if utils.already_applied(flat, args.log):

                    print(f"[{utils.date()}] Oops, we already applied for flat: {flat.title}!")

                elif utils.filter_triggered(flat, user):

                    print(f"[{utils.date()}] Ignoring flat '{flat.title}' because it contains filter keyword(s).")
                
                else:

                    print(f"[{utils.date()}] Applying for flat: {flat.title}..")


                    for email in user.email:
                    
                        click_continue(scrape_flats(driver)[i], driver, float(args.latency_wait))

                        fill_form(email, driver, user, float(args.latency_wait))

                        submit_and_go_back(driver, float(args.latency_wait))


                    utils.log_flat(flat, args.log)


                if i == len(scrape_flats(driver))-1: 
                    prev_page_num = curr_page_num
                    curr_page_num = next_page(curr_page_num, driver, float(args.latency_wait))
                    page_changed = curr_page_num != prev_page_num


        else:

            print(f"[{utils.date()}] Currently no flats available :(")


        if not page_changed:

            time.sleep(float(args.interval) * 60)
            print(f"[{utils.date()}] Reloading main page..")
        
        else:
        
            time.sleep(1.5)


else:

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()