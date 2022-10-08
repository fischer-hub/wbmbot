import os
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from src.user import User
from src.flat import Flat

def init(args):

    chrome_options = Options()
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.headless = args.headless_off
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.implicitly_wait(5)

    curr_page_num = 1
    page_changed = False

    if args.test: 
        print("------------------TEST RUN------------------")
        start_url = f"file://{os.getcwd()}/test-data/wohnung_mehrere_seiten.html"
    else:
        start_url = "https://www.wbm.de/wohnungen-berlin/angebote/"

    if not os.path.isfile(args.log): open(args.log, 'a').close()

    return User(), Flat(), start_url, driver, page_changed, curr_page_num
