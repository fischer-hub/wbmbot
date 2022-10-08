from selenium.webdriver.common.by import By
import time
from src import utils


def accept_cookies(driver, l):
    if len(driver.find_elements(By.XPATH, '//*[@id="cdk-overlay-0"]/div[2]/div[2]/div[2]/button[2]')) > 0:
        driver.find_element(By.XPATH, '//*[@id="cdk-overlay-0"]/div[2]/div[2]/div[2]/button[2]').click()
        time.sleep(l)
        return "Accepting cookies.."
    else:
        return ''


def scrape_flats(driver):
    return driver.find_elements(By.CSS_SELECTOR, ".row.openimmo-search-list-item")


def click_continue(flat_elem, driver, l):
    continue_btn = flat_elem.find_element(By.XPATH, '//*[@title="Details"]')
    continue_btn.location_once_scrolled_into_view
    flat_link = continue_btn.get_attribute('href')
    driver.get(flat_link)
    time.sleep(l)
    return flat_link


def fill_form(email, driver, user, l):
    print(f"[{utils.date()}] Filling out form for email address '{email}'..")
    driver.find_element(By.XPATH, '//*[@id="c722"]/div/div/form/div[2]/div[1]/div/div/div[1]/label').click()
    driver.find_element(By.XPATH, '//*[@id="powermail_field_wbsgueltigbis"]').send_keys(user.wbs_date)
    driver.find_element(By.XPATH, '//*[@id="powermail_field_wbszimmeranzahl"]').send_keys(user.wbs_rooms)
    driver.find_element(By.XPATH, '//*[@id="powermail_field_einkommensgrenzenacheinkommensbescheinigung9"]').send_keys(user.wbs_num)
    driver.find_element(By.XPATH, '//*[@id="powermail_field_name"]').send_keys(user.last_name)
    driver.find_element(By.XPATH, '//*[@id="powermail_field_vorname"]').send_keys(user.first_name)
    driver.find_element(By.XPATH, '//*[@id="powermail_field_strasse"]').send_keys(user.street)
    driver.find_element(By.XPATH, '//*[@id="powermail_field_plz"]').send_keys(user.zip_code)
    driver.find_element(By.XPATH, '//*[@id="powermail_field_ort"]').send_keys(user.city)
    driver.find_element(By.XPATH, '//*[@id="powermail_field_e_mail"]').send_keys(email)
    driver.find_element(By.XPATH, '//*[@id="powermail_field_telefon"]').send_keys(user.phone)
    driver.find_element(By.XPATH, '//*[@id="c722"]/div/div/form/div[2]/div[14]/div/div/div[1]/label').click()
    time.sleep(l)


def submit_and_go_back(driver, l):
    driver.find_element(By.XPATH, '//*[@id="c722"]/div/div/form/div[2]/div[15]/div/div/button').click()
    time.sleep(l)
    driver.back()
    driver.back()
    print(f"[{utils.date()}] Done!")


def next_page(curr_page_num, driver, l):
    if driver.find_elements(By.XPATH, '/html/body/main/div[2]/div[1]/div/nav/ul/li[4]/a'):
        page_list = driver.find_element(By.XPATH, "/html/body/main/div[2]/div[1]/div/nav/ul")
        print(f"[{utils.date()}] Another page of flats was detected, switching to page {curr_page_num +1}/{len(page_list.find_elements(By.TAG_NAME, 'li'))-2}..")
        try:
            page_list.find_elements(By.TAG_NAME, 'li')[curr_page_num + 1].click()
            time.sleep(l)
            return curr_page_num + 1
        except Exception as exc:
            print(f"[{utils.date()}] Failed to switch page, returning to main page..")
            return curr_page_num
    else:
        print(f"[{utils.date()}] Failed to switch page, lastpage reached..")
        return curr_page_num
